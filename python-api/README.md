# FTC Dashboard Python Client

A Python API for interacting with [FTC Dashboard](https://github.com/acmerobotics/ftc-dashboard) via WebSocket connection. This client allows you to read telemetry data and write configuration variables from any Python application.

## Features

- **Read Telemetry**: Stream real-time telemetry data from your robot
- **Write Config Variables**: Update configuration variables on the fly
- **Async/Await API**: Modern Python async API for efficient I/O
- **Event Handlers**: Register callbacks for telemetry, config, and status updates
- **Type Hints**: Full type annotations for better IDE support
- **Easy to Use**: Simple, intuitive API design

## Installation

### From Source

```bash
cd python-api
pip install -e .
```

### Requirements

- Python 3.7+
- websockets library (automatically installed)

## Quick Start

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    # Connect to the dashboard (default: 192.168.49.1:8000)
    async with DashboardClient() as client:
        # Read configuration
        config = await client.get_config()
        print("Current config:", config)
        
        # Update configuration variables
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 1.5,
                "RUN_USING_ENCODER": True
            }
        })
        
        # Read telemetry
        telemetry = await client.get_telemetry(timeout=5.0)
        for packet in telemetry:
            print(f"Telemetry: {packet.data}")

asyncio.run(main())
```

## Usage Examples

### Basic Usage

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    # Connect to dashboard
    # For Android phone: host="192.168.49.1" (default)
    # For Control Hub: host="192.168.43.1"
    async with DashboardClient(host="192.168.49.1", port=8000) as client:
        # Get configuration
        config = await client.get_config(timeout=5.0)
        
        # Update configuration
        await client.save_config({
            "MyCategory": {
                "speed": 0.8,
                "enabled": True
            }
        })
        
        # Read telemetry
        telemetry = await client.get_telemetry(timeout=1.0)
        for packet in telemetry:
            for key, value in packet.data.items():
                print(f"{key}: {value}")

asyncio.run(main())
```

### Continuous Telemetry Monitoring

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    client = DashboardClient()
    
    # Register telemetry handler
    async def on_telemetry(packets):
        for packet in packets:
            print(f"Time: {packet.timestamp}")
            print(f"Data: {packet.data}")
            print(f"Logs: {packet.log}")
    
    client.on_telemetry(on_telemetry)
    
    # Connect and run
    await client.connect()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    finally:
        await client.disconnect()

asyncio.run(main())
```

### Configuration Management

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    async with DashboardClient() as client:
        # Get current configuration
        config = await client.get_config()
        
        # Update single value
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 1.25
            }
        })
        
        # Update multiple values
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 2.0,
                "RUN_USING_ENCODER": True
            },
            "MoreSettings": {
                "Long": 999,
                "Float": 3.14159
            }
        })

asyncio.run(main())
```

## API Reference

### DashboardClient

Main client class for connecting to FTC Dashboard.

#### Constructor

```python
DashboardClient(host="192.168.49.1", port=8000, auto_reconnect=True)
```

**Parameters:**
- `host` (str): Dashboard server hostname or IP address
  - Default: `"192.168.49.1"` (Android phone)
  - Control Hub: `"192.168.43.1"`
- `port` (int): Dashboard server port (default: 8000)
- `auto_reconnect` (bool): Whether to automatically reconnect on connection loss

#### Methods

##### `async connect()`
Establish WebSocket connection to the dashboard.

##### `async disconnect()`
Close the WebSocket connection.

##### `async get_config(timeout=5.0) -> Optional[ConfigVariable]`
Request and wait for configuration from the dashboard.

**Parameters:**
- `timeout` (float): Maximum time to wait for response in seconds

**Returns:** ConfigVariable containing the configuration tree, or None if timeout

##### `async save_config(config_updates: Dict[str, Any])`
Save configuration changes to the dashboard.

**Parameters:**
- `config_updates` (dict): Dictionary of configuration updates (can be nested)

**Example:**
```python
await client.save_config({
    "Category": {
        "variable_name": value
    }
})
```

##### `async get_telemetry(timeout=1.0) -> List[TelemetryPacket]`
Get the latest telemetry data.

**Parameters:**
- `timeout` (float): Maximum time to wait for new telemetry in seconds

**Returns:** List of TelemetryPacket objects

##### `async get_status() -> Optional[RobotStatus]`
Get the latest robot status.

**Returns:** RobotStatus object or None if no status received yet

##### `on_telemetry(handler)`
Register a handler for telemetry updates.

**Parameters:**
- `handler`: Async function that takes a list of TelemetryPacket objects

##### `on_config(handler)`
Register a handler for config updates.

**Parameters:**
- `handler`: Async function that takes a ConfigVariable object

##### `on_status(handler)`
Register a handler for status updates.

**Parameters:**
- `handler`: Async function that takes a RobotStatus object

### TelemetryPacket

Container for telemetry data.

**Attributes:**
- `timestamp` (int): Unix timestamp in milliseconds
- `data` (Dict[str, str]): Dictionary of key-value telemetry data
- `log` (List[str]): List of log messages
- `field` (dict): Field canvas drawing operations
- `fieldOverlay` (dict): Field overlay canvas drawing operations

### ConfigVariable

Represents a configuration variable (basic or nested).

**Attributes:**
- `var_type` (VariableType): Type of the variable
- `value` (Any): Variable value
- `variables` (Optional[Dict]): Nested variables for custom types

### RobotStatus

Robot status information.

**Attributes:**
- `enabled` (bool): Whether robot is enabled
- `available` (bool): Whether robot is available
- `op_mode_name` (str): Name of current OpMode
- `op_mode_status` (str): Status of current OpMode
- `error_message` (str): Error message (if any)
- `warning_message` (str): Warning message (if any)
- `battery_voltage` (float): Battery voltage

## Connection Details

### Default Hosts

- **Android Phone**: `192.168.49.1` (default)
- **Control Hub**: `192.168.43.1`

### Default Port

- `8000`

### WebSocket Protocol

The client communicates with FTC Dashboard using WebSocket protocol with JSON messages. The message format matches the dashboard's Redux action structure.

## Examples

Check the `examples/` directory for more detailed examples:

- `basic_usage.py` - Basic connection, config, and telemetry reading
- `telemetry_monitor.py` - Continuous telemetry monitoring with handlers
- `config_editor.py` - Interactive configuration editing

## Running Examples

```bash
# From the python-api directory
cd examples

# Install the client first (from python-api directory)
cd ..
pip install -e .

# Run an example
cd examples
python basic_usage.py
```

**Note:** Make sure your FTC Dashboard server is running and accessible before running examples.

## Troubleshooting

### Connection Issues

1. **Check network connectivity**: Ensure your computer is on the same network as the robot
2. **Verify the host**: Use the correct IP address for your setup
   - Android phone: `192.168.49.1`
   - Control Hub: `192.168.43.1`
3. **Check port**: Default port is `8000`
4. **Firewall**: Ensure no firewall is blocking WebSocket connections

### Import Errors

Make sure the `websockets` package is installed:
```bash
pip install websockets
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Style

This project uses `black` for code formatting:
```bash
black ftc_dashboard_client
```

### Type Checking

```bash
mypy ftc_dashboard_client
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project follows the same license as FTC Dashboard. See the main repository for details.

## Links

- [FTC Dashboard](https://github.com/acmerobotics/ftc-dashboard)
- [FTC Dashboard Documentation](https://acmerobotics.github.io/ftc-dashboard)
