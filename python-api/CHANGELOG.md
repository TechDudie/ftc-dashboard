# Changelog

All notable changes to the FTC Dashboard Python Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-20

### Added
- Initial release of FTC Dashboard Python Client
- WebSocket client for connecting to FTC Dashboard
- Async/await API for modern Python applications
- Full type hints and dataclass models
- Support for reading telemetry data
  - `get_telemetry()` method for one-time reads
  - `on_telemetry()` handler for continuous monitoring
  - TelemetryPacket dataclass with full field support
- Support for reading and writing configuration variables
  - `get_config()` method to retrieve configuration
  - `save_config()` method to update variables
  - ConfigVariable dataclass supporting all types (int, float, bool, string, custom)
  - Nested configuration support
- Robot status monitoring
  - `get_status()` method
  - `on_status()` handler
  - RobotStatus dataclass
- Event handler registration system
  - `on_telemetry()` for telemetry updates
  - `on_config()` for config updates
  - `on_status()` for status updates
- Automatic reconnection support
- Comprehensive documentation
  - README.md with full API documentation
  - INSTALL.md with installation guide
  - examples/README.md with example descriptions
- Example scripts
  - basic_usage.py - Basic API usage
  - telemetry_monitor.py - Continuous monitoring
  - config_editor.py - Configuration management
  - data_logger.py - CSV data logging
  - test_with_server.py - Integration tests
- Unit tests (test_client.py)
- Package setup (setup.py, requirements.txt)
- Type definitions for all message types
  - MessageType enum
  - VariableType enum
  - DrawOp types for canvas operations

### Dependencies
- websockets >= 10.0

### Supported Python Versions
- Python 3.7+
- Python 3.8+
- Python 3.9+
- Python 3.10+
- Python 3.11+
- Python 3.12+

### Known Limitations
- Canvas drawing operations are received but not yet fully documented
- Image streaming (RECEIVE_IMAGE) is defined but not yet implemented
- OpMode controls (INIT_OP_MODE, START_OP_MODE, STOP_OP_MODE) are not exposed in the public API
- Gamepad state (RECEIVE_GAMEPAD_STATE) is not exposed in the public API
- Hardware config operations are not exposed in the public API

### Notes
- This is the first release focused on the core use case: reading telemetry and writing config variables
- Additional features may be added in future releases based on user feedback
- The WebSocket protocol matches the browser client implementation
- Message format is compatible with FTC Dashboard 0.5.1+

## [Unreleased]

### Planned Features
- Synchronous API wrapper for non-async code
- OpMode control methods
- Camera/image streaming support
- Gamepad state monitoring
- Hardware configuration management
- Field canvas rendering utilities
- More comprehensive examples
- pytest-based test suite
- Type stub files for better IDE support
- Optional dependencies for data analysis (pandas, numpy)
