# Quick Start Guide - FTC Dashboard Python Client

Get up and running with the FTC Dashboard Python Client in 5 minutes!

## 1. Install

```bash
cd ftc-dashboard/python-api
pip install -e .
```

## 2. Connect to Your Robot

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    # For Android Phone (default)
    async with DashboardClient() as client:
        print("Connected!")

asyncio.run(main())
```

**For Control Hub**, change the host:
```python
async with DashboardClient(host="192.168.43.1") as client:
```

## 3. Read Telemetry

```python
async def main():
    async with DashboardClient() as client:
        # Get latest telemetry
        telemetry = await client.get_telemetry(timeout=2.0)
        
        for packet in telemetry:
            print(f"Timestamp: {packet.timestamp}")
            for key, value in packet.data.items():
                print(f"  {key}: {value}")

asyncio.run(main())
```

## 4. Update Configuration

```python
async def main():
    async with DashboardClient() as client:
        # Update config variables
        await client.save_config({
            "MyCategory": {
                "speed": 1.5,
                "enabled": True,
                "name": "robot"
            }
        })
        print("Configuration updated!")

asyncio.run(main())
```

## 5. Read Configuration

```python
async def main():
    async with DashboardClient() as client:
        # Get current configuration
        config = await client.get_config()
        
        if config and config.variables:
            for category, var in config.variables.items():
                print(f"{category}:")
                if var.variables:
                    for name, value in var.variables.items():
                        print(f"  {name}: {value.value}")

asyncio.run(main())
```

## 6. Monitor Telemetry Continuously

```python
async def main():
    client = DashboardClient()
    
    # Register a handler
    async def on_telemetry(packets):
        for packet in packets:
            print(f"Data: {packet.data}")
    
    client.on_telemetry(on_telemetry)
    
    await client.connect()
    
    try:
        # Run forever (or until Ctrl+C)
        while True:
            await asyncio.sleep(1)
    finally:
        await client.disconnect()

asyncio.run(main())
```

## Common Patterns

### Check Robot Status

```python
async with DashboardClient() as client:
    status = await client.get_status()
    print(f"Robot enabled: {status.enabled}")
    print(f"Battery: {status.battery_voltage}V")
    print(f"OpMode: {status.op_mode_name}")
```

### Update Multiple Config Values

```python
await client.save_config({
    "Category1": {
        "var1": 1.5,
        "var2": True
    },
    "Category2": {
        "var3": "hello",
        "var4": 42
    }
})
```

### Log Telemetry to File

```python
import csv

log_file = open("telemetry.csv", "w", newline="")
writer = csv.writer(log_file)

async def on_telemetry(packets):
    for packet in packets:
        if packet.data:
            row = [packet.timestamp] + list(packet.data.values())
            writer.writerow(row)
            log_file.flush()

client.on_telemetry(on_telemetry)
```

## Connection Settings

| Device | Host | Port |
|--------|------|------|
| Android Phone | `192.168.49.1` | `8000` |
| Control Hub | `192.168.43.1` | `8000` |

## Troubleshooting

**Can't connect?**
- Check you're on the robot's Wi-Fi network
- Verify the correct IP address
- Ensure FTC Dashboard is running

**No telemetry?**
- Make sure an OpMode is running
- Check that telemetry is being sent in robot code

**Import error?**
```bash
pip install websockets
```

## Next Steps

- Read the full [README.md](README.md) for complete API documentation
- Try the [examples](examples/) for more patterns
- Check [INSTALL.md](INSTALL.md) for detailed installation help

## Complete Example

Here's a complete example combining everything:

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    async with DashboardClient(host="192.168.49.1") as client:
        # Get status
        status = await client.get_status()
        if status:
            print(f"Robot: {status.op_mode_name} ({status.battery_voltage}V)")
        
        # Get config
        config = await client.get_config()
        if config:
            print(f"Config categories: {list(config.variables.keys())}")
        
        # Update config
        await client.save_config({
            "Test": {"speed": 1.5}
        })
        print("Config updated!")
        
        # Get telemetry
        telemetry = await client.get_telemetry(timeout=2.0)
        if telemetry:
            print(f"Received {len(telemetry)} telemetry packet(s)")
            for packet in telemetry:
                print(f"  Data: {packet.data}")

if __name__ == "__main__":
    asyncio.run(main())
```

Save as `my_script.py` and run:
```bash
python my_script.py
```

That's it! You're ready to start using the FTC Dashboard Python Client! 🚀
