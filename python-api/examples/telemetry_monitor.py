"""
Continuous telemetry monitoring example.

This example demonstrates how to continuously monitor telemetry
using event handlers.
"""

import asyncio
import logging
from ftc_dashboard_client import DashboardClient, TelemetryPacket

logging.basicConfig(level=logging.INFO)


async def main():
    # Create client
    client = DashboardClient(host="192.168.49.1", port=8000)
    
    # Register telemetry handler
    async def on_telemetry_received(packets: list):
        for packet in packets:
            print(f"\n=== Telemetry Update (timestamp: {packet.timestamp}) ===")
            
            # Print all data fields
            if packet.data:
                print("Data:")
                for key, value in packet.data.items():
                    print(f"  {key}: {value}")
            
            # Print log messages
            if packet.log:
                print("Logs:")
                for log_msg in packet.log:
                    print(f"  {log_msg}")
    
    # Register handler
    client.on_telemetry(on_telemetry_received)
    
    # Connect and run
    await client.connect()
    
    try:
        print("Monitoring telemetry... Press Ctrl+C to stop")
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
