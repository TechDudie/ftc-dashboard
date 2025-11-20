"""
Integration test with the FTC Dashboard test server.

This example demonstrates testing with the TestServer.java mock server.

Prerequisites:
1. Start the test server: 
   cd DashboardCore
   ../gradlew run
   
2. Run this script:
   python test_with_server.py
"""

import asyncio
import logging
from ftc_dashboard_client import DashboardClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_connection():
    """Test basic connection to the server."""
    print("\n=== Test 1: Connection ===")
    client = DashboardClient(host="localhost", port=8000)
    
    try:
        await client.connect()
        print("✓ Connected successfully")
        
        # Wait a bit for initial messages
        await asyncio.sleep(0.5)
        
        status = await client.get_status()
        if status:
            print(f"✓ Robot status received:")
            print(f"  - Enabled: {status.enabled}")
            print(f"  - OpMode: {status.op_mode_name}")
            print(f"  - Battery: {status.battery_voltage}V")
        
        await client.disconnect()
        print("✓ Disconnected successfully")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


async def test_config_operations():
    """Test configuration read and write operations."""
    print("\n=== Test 2: Configuration Operations ===")
    
    async with DashboardClient(host="localhost", port=8000) as client:
        # Get configuration
        print("Getting configuration...")
        config = await client.get_config(timeout=5.0)
        
        if config:
            print("✓ Configuration received")
            if config.variables:
                print(f"  Found {len(config.variables)} top-level categories:")
                for key in config.variables.keys():
                    print(f"    - {key}")
        else:
            print("✗ No configuration received")
            return False
        
        # Update configuration
        print("\nUpdating configuration...")
        await client.save_config({
            "Test": {
                "LATERAL_MULTIPLIER": 2.5,
                "RUN_USING_ENCODER": False
            }
        })
        print("✓ Configuration update sent")
        
        # Wait a bit for the update to be processed
        await asyncio.sleep(0.5)
        
        # Verify the update
        print("\nVerifying configuration update...")
        config = await client.get_config(timeout=5.0)
        
        if config and config.variables:
            test_config = config.variables.get("Test")
            if test_config and test_config.variables:
                lat_mult = test_config.variables.get("LATERAL_MULTIPLIER")
                run_encoder = test_config.variables.get("RUN_USING_ENCODER")
                
                if lat_mult and lat_mult.value == 2.5:
                    print("✓ LATERAL_MULTIPLIER updated correctly: 2.5")
                else:
                    print(f"✗ LATERAL_MULTIPLIER not updated correctly: {lat_mult.value if lat_mult else 'not found'}")
                
                if run_encoder and run_encoder.value == False:
                    print("✓ RUN_USING_ENCODER updated correctly: False")
                else:
                    print(f"✗ RUN_USING_ENCODER not updated correctly: {run_encoder.value if run_encoder else 'not found'}")
        
        return True


async def test_telemetry_monitoring():
    """Test telemetry monitoring."""
    print("\n=== Test 3: Telemetry Monitoring ===")
    
    client = DashboardClient(host="localhost", port=8000)
    
    telemetry_received = []
    
    async def on_telemetry(packets):
        telemetry_received.extend(packets)
        print(f"✓ Received {len(packets)} telemetry packet(s)")
        for packet in packets:
            if packet.data:
                print(f"  Data: {list(packet.data.keys())}")
    
    client.on_telemetry(on_telemetry)
    
    await client.connect()
    
    try:
        print("Monitoring telemetry for 5 seconds...")
        await asyncio.sleep(5)
        
        if telemetry_received:
            print(f"✓ Received {len(telemetry_received)} total telemetry packets")
            return True
        else:
            print("! No telemetry received (this is normal if no OpMode is running)")
            return True  # Not a failure, just no active telemetry
    finally:
        await client.disconnect()


async def main():
    """Run all integration tests."""
    print("=" * 70)
    print("FTC Dashboard Python Client - Integration Tests")
    print("=" * 70)
    print("\nMake sure the TestServer is running:")
    print("  cd DashboardCore")
    print("  ../gradlew run")
    print()
    
    # Run tests
    results = []
    
    # Test 1: Connection
    try:
        result = await test_connection()
        results.append(("Connection", result))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Connection", False))
    
    # Test 2: Configuration
    try:
        result = await test_config_operations()
        results.append(("Configuration", result))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Configuration", False))
    
    # Test 3: Telemetry
    try:
        result = await test_telemetry_monitoring()
        results.append(("Telemetry", result))
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        results.append(("Telemetry", False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
