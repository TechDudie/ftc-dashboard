# FTC Dashboard Python Client - Examples

This directory contains example scripts demonstrating various uses of the FTC Dashboard Python Client.

## Prerequisites

Install the client library:
```bash
cd python-api
pip install -e .
```

## Examples

### 1. basic_usage.py
**Basic usage of the client API**

Demonstrates:
- Connecting to the dashboard
- Reading configuration
- Updating configuration variables
- Reading telemetry data
- Getting robot status

```bash
python basic_usage.py
```

### 2. telemetry_monitor.py
**Continuous telemetry monitoring**

Demonstrates:
- Registering event handlers for telemetry updates
- Continuous monitoring of telemetry data
- Handling telemetry packets in real-time

```bash
python telemetry_monitor.py
```

Press Ctrl+C to stop monitoring.

### 3. config_editor.py
**Interactive configuration editor**

Demonstrates:
- Reading the full configuration tree
- Updating single and multiple configuration values
- Verifying configuration changes

```bash
python config_editor.py
```

### 4. data_logger.py
**Telemetry data logging to CSV**

Demonstrates:
- Logging telemetry data to a CSV file
- Automated data collection for analysis
- Timestamped log files

```bash
python data_logger.py
```

This will create a `telemetry_logs/` directory with timestamped CSV files.

### 5. test_with_server.py
**Integration testing with TestServer**

Demonstrates:
- Testing connection to the dashboard
- Testing configuration operations
- Testing telemetry monitoring
- Comprehensive integration testing

**Prerequisites:**
1. Start the TestServer:
   ```bash
   cd DashboardCore
   ../gradlew run
   ```

2. Run the test:
   ```bash
   python test_with_server.py
   ```

## Configuration

All examples use these default connection settings:
- **Android Phone**: `host="192.168.49.1"` (default)
- **Control Hub**: `host="192.168.43.1"`
- **Port**: `8000`

You can modify these in each example script as needed.

## Troubleshooting

### Connection Refused
- Ensure the FTC Dashboard is running
- Check that you're using the correct IP address
- Verify you're on the same network as the robot

### No Telemetry Received
- Ensure an OpMode is running that sends telemetry
- Check that telemetry is being sent from the robot code
- For testing, use the TestServer which includes sample telemetry

### Import Errors
```bash
pip install websockets
```

## Creating Your Own Examples

Here's a minimal template to get started:

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    async with DashboardClient(host="192.168.49.1") as client:
        # Your code here
        pass

if __name__ == "__main__":
    asyncio.run(main())
```

## More Information

For full API documentation, see the main [README.md](../README.md).
