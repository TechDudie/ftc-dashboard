"""
Main client implementation for FTC Dashboard WebSocket connection.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Awaitable
from collections import defaultdict

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
except ImportError:
    raise ImportError(
        "websockets package is required. Install it with: pip install websockets"
    )

from .types import (
    ConfigVariable,
    MessageType,
    RobotStatus,
    TelemetryPacket,
)


logger = logging.getLogger(__name__)


class DashboardClient:
    """
    Client for connecting to FTC Dashboard via WebSocket.
    
    This client allows you to:
    - Read telemetry data from the robot
    - Read and write configuration variables
    - Monitor robot status
    
    Example:
        ```python
        import asyncio
        from ftc_dashboard_client import DashboardClient
        
        async def main():
            # Connect to dashboard (default: 192.168.49.1:8000)
            async with DashboardClient() as client:
                # Get configuration
                config = await client.get_config()
                print("Current config:", config)
                
                # Update a config variable
                await client.save_config({
                    "Test": {
                        "LATERAL_MULTIPLIER": 1.5
                    }
                })
                
                # Read telemetry
                telemetry = await client.get_telemetry(timeout=5.0)
                for packet in telemetry:
                    print(f"Telemetry: {packet.data}")
        
        asyncio.run(main())
        ```
    """
    
    def __init__(
        self,
        host: str = "192.168.49.1",
        port: int = 8000,
        auto_reconnect: bool = True
    ):
        """
        Initialize the dashboard client.
        
        Args:
            host: Dashboard server hostname or IP (default: 192.168.49.1 for Android phone)
            port: Dashboard server port (default: 8000)
            auto_reconnect: Whether to automatically reconnect on connection loss
        """
        self.host = host
        self.port = port
        self.auto_reconnect = auto_reconnect
        self.ws: Optional[WebSocketClientProtocol] = None
        
        # Message handlers
        self._telemetry_handlers: List[Callable[[List[TelemetryPacket]], Awaitable[None]]] = []
        self._config_handlers: List[Callable[[ConfigVariable], Awaitable[None]]] = []
        self._status_handlers: List[Callable[[RobotStatus], Awaitable[None]]] = []
        
        # State
        self._connected = False
        self._receive_task: Optional[asyncio.Task] = None
        self._latest_telemetry: List[TelemetryPacket] = []
        self._latest_config: Optional[ConfigVariable] = None
        self._latest_status: Optional[RobotStatus] = None
        
        # Pending responses for request-response pattern
        self._pending_config_response: Optional[asyncio.Future] = None
    
    @property
    def connected(self) -> bool:
        """Check if the client is connected to the dashboard."""
        return self._connected and self.ws is not None and not self.ws.closed
    
    async def connect(self):
        """Establish WebSocket connection to the dashboard."""
        uri = f"ws://{self.host}:{self.port}"
        logger.info(f"Connecting to dashboard at {uri}")
        
        try:
            self.ws = await websockets.connect(uri)
            self._connected = True
            logger.info("Connected to dashboard")
            
            # Start receiving messages
            self._receive_task = asyncio.create_task(self._receive_loop())
            
            # Send initial status request
            await self._send_message({"type": MessageType.GET_ROBOT_STATUS.value})
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def disconnect(self):
        """Close the WebSocket connection."""
        logger.info("Disconnecting from dashboard")
        self._connected = False
        
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        
        if self.ws:
            await self.ws.close()
            self.ws = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
    
    async def _send_message(self, message: Dict[str, Any]):
        """Send a message to the dashboard."""
        if not self.connected:
            raise RuntimeError("Not connected to dashboard")
        
        message_str = json.dumps(message)
        logger.debug(f"Sending message: {message_str}")
        await self.ws.send(message_str)
    
    async def _receive_loop(self):
        """Main loop for receiving and processing messages."""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
        except asyncio.CancelledError:
            logger.debug("Receive loop cancelled")
        except Exception as e:
            logger.error(f"Receive loop error: {e}")
            if self.auto_reconnect:
                logger.info("Attempting to reconnect...")
                await asyncio.sleep(1)
                try:
                    await self.connect()
                except Exception as reconnect_error:
                    logger.error(f"Reconnection failed: {reconnect_error}")
    
    async def _handle_message(self, data: Dict[str, Any]):
        """Handle incoming messages from the dashboard."""
        msg_type = data.get('type')
        logger.debug(f"Received message type: {msg_type}")
        
        if msg_type == MessageType.RECEIVE_TELEMETRY.value:
            await self._handle_telemetry(data)
        elif msg_type == MessageType.RECEIVE_CONFIG.value:
            await self._handle_config(data)
        elif msg_type == MessageType.RECEIVE_ROBOT_STATUS.value:
            await self._handle_status(data)
        else:
            logger.debug(f"Unhandled message type: {msg_type}")
    
    async def _handle_telemetry(self, data: Dict[str, Any]):
        """Handle incoming telemetry messages."""
        telemetry_list = data.get('telemetry', [])
        packets = [TelemetryPacket.from_dict(t) for t in telemetry_list]
        
        self._latest_telemetry = packets
        
        # Call registered handlers
        for handler in self._telemetry_handlers:
            try:
                await handler(packets)
            except Exception as e:
                logger.error(f"Error in telemetry handler: {e}")
    
    async def _handle_config(self, data: Dict[str, Any]):
        """Handle incoming config messages."""
        config_root = data.get('configRoot')
        if config_root:
            config = ConfigVariable.from_dict(config_root)
            self._latest_config = config
            
            # Resolve pending request
            if self._pending_config_response and not self._pending_config_response.done():
                self._pending_config_response.set_result(config)
            
            # Call registered handlers
            for handler in self._config_handlers:
                try:
                    await handler(config)
                except Exception as e:
                    logger.error(f"Error in config handler: {e}")
    
    async def _handle_status(self, data: Dict[str, Any]):
        """Handle incoming status messages."""
        status_data = data.get('robotStatus', {})
        status = RobotStatus.from_dict(status_data)
        self._latest_status = status
        
        # Call registered handlers
        for handler in self._status_handlers:
            try:
                await handler(status)
            except Exception as e:
                logger.error(f"Error in status handler: {e}")
    
    # Public API methods
    
    async def get_config(self, timeout: float = 5.0) -> Optional[ConfigVariable]:
        """
        Request and wait for configuration from the dashboard.
        
        Args:
            timeout: Maximum time to wait for response in seconds
            
        Returns:
            ConfigVariable containing the configuration tree, or None if timeout
        """
        if not self.connected:
            raise RuntimeError("Not connected to dashboard")
        
        # Create a future for the response
        self._pending_config_response = asyncio.Future()
        
        # Send request
        await self._send_message({"type": MessageType.GET_CONFIG.value})
        
        # Wait for response
        try:
            config = await asyncio.wait_for(self._pending_config_response, timeout=timeout)
            return config
        except asyncio.TimeoutError:
            logger.warning("Config request timed out")
            return None
        finally:
            self._pending_config_response = None
    
    async def save_config(self, config_updates: Dict[str, Any]):
        """
        Save configuration changes to the dashboard.
        
        Args:
            config_updates: Dictionary of configuration updates.
                           Can be nested to match the config structure.
                           
        Example:
            ```python
            await client.save_config({
                "Test": {
                    "LATERAL_MULTIPLIER": 1.5,
                    "RUN_USING_ENCODER": True
                }
            })
            ```
        """
        if not self.connected:
            raise RuntimeError("Not connected to dashboard")
        
        # Convert dictionary to ConfigVariable structure
        def dict_to_config(d: Dict[str, Any]) -> ConfigVariable:
            variables = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    variables[key] = dict_to_config(value)
                else:
                    variables[key] = ConfigVariable.create_basic(value)
            return ConfigVariable.create_custom(variables)
        
        config_diff = dict_to_config(config_updates)
        
        # Send save request
        message = {
            "type": MessageType.SAVE_CONFIG.value,
            "configDiff": config_diff.to_dict()
        }
        await self._send_message(message)
    
    async def get_telemetry(self, timeout: float = 1.0) -> List[TelemetryPacket]:
        """
        Get the latest telemetry data.
        
        Args:
            timeout: Maximum time to wait for new telemetry in seconds
            
        Returns:
            List of TelemetryPacket objects
        """
        if not self.connected:
            raise RuntimeError("Not connected to dashboard")
        
        # Clear existing telemetry
        self._latest_telemetry = []
        
        # Wait for new telemetry
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            if self._latest_telemetry:
                return self._latest_telemetry
            await asyncio.sleep(0.1)
        
        return self._latest_telemetry
    
    async def get_status(self) -> Optional[RobotStatus]:
        """
        Get the latest robot status.
        
        Returns:
            RobotStatus object or None if no status received yet
        """
        if not self.connected:
            raise RuntimeError("Not connected to dashboard")
        
        await self._send_message({"type": MessageType.GET_ROBOT_STATUS.value})
        
        # Wait a bit for response
        await asyncio.sleep(0.1)
        
        return self._latest_status
    
    # Handler registration methods
    
    def on_telemetry(self, handler: Callable[[List[TelemetryPacket]], Awaitable[None]]):
        """
        Register a handler for telemetry updates.
        
        Args:
            handler: Async function that takes a list of TelemetryPacket objects
        """
        self._telemetry_handlers.append(handler)
    
    def on_config(self, handler: Callable[[ConfigVariable], Awaitable[None]]):
        """
        Register a handler for config updates.
        
        Args:
            handler: Async function that takes a ConfigVariable object
        """
        self._config_handlers.append(handler)
    
    def on_status(self, handler: Callable[[RobotStatus], Awaitable[None]]):
        """
        Register a handler for status updates.
        
        Args:
            handler: Async function that takes a RobotStatus object
        """
        self._status_handlers.append(handler)
