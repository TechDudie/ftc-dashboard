# Installation Guide - FTC Dashboard Python Client

This guide provides detailed installation instructions for the FTC Dashboard Python Client.

## Prerequisites

- **Python**: Version 3.7 or higher
- **pip**: Python package installer (usually comes with Python)
- **Network Access**: Connection to the robot's network

## Quick Install

### From Source (Recommended for Development)

1. Clone the repository or download the source:
   ```bash
   git clone https://github.com/acmerobotics/ftc-dashboard.git
   cd ftc-dashboard/python-api
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

   This installs the package in "editable" mode, allowing you to modify the code and see changes immediately.

### Standard Install

Install directly from the source directory:
```bash
cd ftc-dashboard/python-api
pip install .
```

## Verify Installation

Test that the installation was successful:

```bash
python -c "from ftc_dashboard_client import DashboardClient; print('✓ Installation successful!')"
```

## Dependencies

The only external dependency is `websockets`:
- websockets >= 10.0

This will be automatically installed when you install the package.

### Manual Dependency Installation

If needed, install dependencies manually:
```bash
pip install -r requirements.txt
```

## Platform-Specific Instructions

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt or PowerShell
3. Navigate to the python-api directory
4. Run the installation commands above

### macOS

Python 3 is usually pre-installed. If not:
```bash
brew install python3
```

Then follow the standard installation steps.

### Linux

Python 3 is typically pre-installed. Ensure pip is installed:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# Fedora
sudo dnf install python3-pip

# Arch
sudo pacman -S python-pip
```

Then follow the standard installation steps.

## Virtual Environments (Recommended)

Using a virtual environment keeps the installation isolated:

### Using venv

```bash
# Create virtual environment
python -m venv ftc-env

# Activate it
# On Windows:
ftc-env\Scripts\activate
# On macOS/Linux:
source ftc-env/bin/activate

# Install the package
pip install -e .
```

### Using conda

```bash
# Create environment
conda create -n ftc python=3.11

# Activate it
conda activate ftc

# Install the package
pip install -e .
```

## Testing the Installation

Run the included tests:
```bash
cd python-api
python test_client.py
```

Expected output:
```
============================================================
Running FTC Dashboard Python Client Tests
============================================================

✓ TelemetryPacket.from_dict() works correctly
✓ ConfigVariable.create_basic() works correctly
✓ ConfigVariable.create_custom() works correctly
✓ ConfigVariable.from_dict() works correctly
✓ RobotStatus.from_dict() works correctly
✓ DashboardClient initialization works correctly
✓ All MessageType constants are defined

============================================================
✓ All tests passed!
============================================================
```

## Network Configuration

### Finding Your Robot's IP Address

**Android Phone (Wi-Fi Direct):**
- Default IP: `192.168.49.1`
- Port: `8000`

**Control Hub:**
- Default IP: `192.168.43.1`
- Port: `8000`

### Testing Network Connectivity

```bash
# Test if the robot is reachable
ping 192.168.49.1
```

## Running Examples

After installation, try the examples:

```bash
cd examples
python basic_usage.py
```

See [examples/README.md](examples/README.md) for more information.

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'websockets'`

**Solution:**
```bash
pip install websockets
```

### Connection Errors

**Problem:** `ConnectionRefusedError` or timeout when connecting

**Solutions:**
1. Verify the robot is powered on
2. Check you're connected to the robot's Wi-Fi network
3. Verify the IP address is correct
4. Ensure the FTC Dashboard is running on the robot
5. Check firewall settings

### Permission Errors

**Problem:** Permission denied when installing

**Solution:**
Use `--user` flag:
```bash
pip install --user -e .
```

Or use a virtual environment (recommended).

### Python Version Issues

**Problem:** `SyntaxError` or incompatible features

**Solution:**
Ensure you're using Python 3.7 or higher:
```bash
python --version
```

If needed, use `python3` explicitly:
```bash
python3 -m pip install -e .
```

## Uninstallation

To remove the package:
```bash
pip uninstall ftc-dashboard-client
```

## Development Setup

For development with additional tools:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# This includes:
# - pytest (testing)
# - pytest-asyncio (async testing)
# - black (code formatting)
# - mypy (type checking)
```

## Getting Help

- Check the [README.md](README.md) for API documentation
- Review the [examples/](examples/) directory for usage patterns
- Visit the main [FTC Dashboard repository](https://github.com/acmerobotics/ftc-dashboard)

## Next Steps

After installation:
1. Review the [README.md](README.md) for API documentation
2. Try the examples in [examples/](examples/)
3. Read the [examples/README.md](examples/README.md) for example descriptions
4. Start building your own scripts!

## Minimal Example

Test your installation with this minimal example:

```python
import asyncio
from ftc_dashboard_client import DashboardClient

async def main():
    async with DashboardClient(host="192.168.49.1") as client:
        status = await client.get_status()
        print(f"Connected! Robot enabled: {status.enabled if status else 'unknown'}")

asyncio.run(main())
```

Save as `test_connection.py` and run:
```bash
python test_connection.py
```
