"""
Interactive configuration editor example.

This example demonstrates how to read and modify configuration
variables interactively.
"""

import asyncio
import logging
from ftc_dashboard_client import DashboardClient, ConfigVariable, VariableType

logging.basicConfig(level=logging.INFO)


def print_config(config: ConfigVariable, indent: int = 0):
    """Recursively print configuration structure."""
    if config.var_type == VariableType.CUSTOM and config.variables:
        for key, var in config.variables.items():
            if var.var_type == VariableType.CUSTOM:
                print("  " * indent + f"{key}:")
                print_config(var, indent + 1)
            else:
                print("  " * indent + f"{key}: {var.value} (type: {var.var_type.value})")
    else:
        print("  " * indent + f"Value: {config.value}")


async def main():
    async with DashboardClient(host="192.168.49.1", port=8000) as client:
        print("Connected to FTC Dashboard!")
        print("=" * 60)
        
        # Get and display current configuration
        print("\n--- Current Configuration ---")
        config = await client.get_config(timeout=5.0)
        
        if config:
            print_config(config)
        else:
            print("No configuration available")
            return
        
        print("\n" + "=" * 60)
        print("Configuration Editor")
        print("=" * 60)
        
        # Example: Update specific variables
        print("\nExample 1: Update a numeric value")
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 1.25
            }
        })
        print("✓ Updated Test.LATERAL_MULTIPLIER to 1.25")
        
        print("\nExample 2: Update a boolean value")
        await client.save_config({
            "Test": {
                "RUN_USING_ENCODER": False
            }
        })
        print("✓ Updated Test.RUN_USING_ENCODER to False")
        
        print("\nExample 3: Update multiple values at once")
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 2.0,
                "RUN_USING_ENCODER": True
            },
            "More Primitives": {
                "Long": 999,
                "Float": 3.14159
            }
        })
        print("✓ Updated multiple configuration values")
        
        # Verify changes
        print("\n--- Verifying Changes ---")
        await asyncio.sleep(0.5)  # Wait a bit for updates to propagate
        config = await client.get_config(timeout=5.0)
        
        if config:
            print_config(config)
        
        print("\nConfiguration updates completed!")


if __name__ == "__main__":
    asyncio.run(main())
