"""
FTC Dashboard Python Client

A Python API for interacting with FTC Dashboard via WebSocket connection.
Provides functionality to read telemetry and write configuration variables.
"""

from .client import DashboardClient
from .types import (
    TelemetryPacket,
    ConfigVariable,
    RobotStatus,
    VariableType,
    MessageType
)

__version__ = "0.1.0"
__all__ = [
    "DashboardClient",
    "TelemetryPacket",
    "ConfigVariable",
    "RobotStatus",
    "VariableType",
    "MessageType"
]
