"""
Basic usage example for FTC Dashboard Python Client.

This example demonstrates:
1. Connecting to the dashboard
2. Reading configuration
3. Updating configuration variables
4. Reading telemetry data
"""

import asyncio
import logging
from ftc_dashboard_client import DashboardClient

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)


async def main():
    # Connect to the dashboard
    # Default host is 192.168.49.1 (Android phone)
    # Use 192.168.43.1 for Control Hub
    async with DashboardClient(host="192.168.49.1", port=8000) as client:
        print("Connected to FTC Dashboard!")
        
        # Get current configuration
        print("\n--- Getting Configuration ---")
        config = await client.get_config(timeout=5.0)
        
        if config:
            print(f"Configuration received: {config.var_type}")
            if config.variables:
                for key, var in config.variables.items():
                    print(f"  {key}: {var.value}")
        else:
            print("No configuration received")
        
        # Update a configuration variable
        print("\n--- Updating Configuration ---")
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 1.5,
                "RUN_USING_ENCODER": True
            }
        })
        print("Configuration updated!")
        
        # Read telemetry for 5 seconds
        print("\n--- Reading Telemetry ---")
        for i in range(5):
            telemetry = await client.get_telemetry(timeout=1.0)
            
            if telemetry:
                for packet in telemetry:
                    print(f"Telemetry at {packet.timestamp}:")
                    for key, value in packet.data.items():
                        print(f"  {key}: {value}")
                    if packet.log:
                        print(f"  Logs: {packet.log}")
            else:
                print(f"No telemetry received (attempt {i+1}/5)")
            
            await asyncio.sleep(1)
        
        # Get robot status
        print("\n--- Robot Status ---")
        status = await client.get_status()
        if status:
            print(f"Robot enabled: {status.enabled}")
            print(f"OpMode: {status.op_mode_name}")
            print(f"Battery: {status.battery_voltage}V")


if __name__ == "__main__":
    asyncio.run(main())
