"""
Type definitions for FTC Dashboard messages and data structures.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class MessageType(str, Enum):
    """Dashboard message types matching the Java MessageType enum."""
    GET_ROBOT_STATUS = "GET_ROBOT_STATUS"
    RECEIVE_ROBOT_STATUS = "RECEIVE_ROBOT_STATUS"
    INIT_OP_MODE = "INIT_OP_MODE"
    START_OP_MODE = "START_OP_MODE"
    STOP_OP_MODE = "STOP_OP_MODE"
    RECEIVE_OP_MODE_LIST = "RECEIVE_OP_MODE_LIST"
    GET_CONFIG = "GET_CONFIG"
    SAVE_CONFIG = "SAVE_CONFIG"
    RECEIVE_CONFIG = "RECEIVE_CONFIG"
    RECEIVE_TELEMETRY = "RECEIVE_TELEMETRY"
    RECEIVE_IMAGE = "RECEIVE_IMAGE"
    RECEIVE_GAMEPAD_STATE = "RECEIVE_GAMEPAD_STATE"
    RECEIVE_HARDWARE_CONFIG_LIST = "RECEIVE_HARDWARE_CONFIG_LIST"
    SET_HARDWARE_CONFIG = "SET_HARDWARE_CONFIG"


class VariableType(str, Enum):
    """Configuration variable types."""
    CUSTOM = "custom"
    BOOLEAN = "boolean"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    ENUM = "enum"
    READONLY_STRING = "readonly_string"


@dataclass
class DrawOp:
    """Base class for canvas drawing operations."""
    type: str


@dataclass
class TelemetryPacket:
    """
    Container for telemetry data received from the robot.
    
    Attributes:
        timestamp: Unix timestamp in milliseconds
        data: Dictionary of key-value telemetry data
        log: List of log messages
        field: Field canvas drawing operations
        fieldOverlay: Field overlay canvas drawing operations
    """
    timestamp: int
    data: Dict[str, str]
    log: List[str]
    field: Dict[str, List[DrawOp]]
    fieldOverlay: Dict[str, List[DrawOp]]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TelemetryPacket':
        """Create a TelemetryPacket from a dictionary."""
        return cls(
            timestamp=data.get('timestamp', 0),
            data=data.get('data', {}),
            log=data.get('log', []),
            field=data.get('field', {'ops': []}),
            fieldOverlay=data.get('fieldOverlay', {'ops': []})
        )


@dataclass
class ConfigVariable:
    """
    Represents a configuration variable.
    
    This can be either a basic variable (int, float, string, etc.) or
    a custom variable containing nested variables.
    """
    var_type: VariableType
    value: Any
    enum_class: Optional[str] = None
    enum_values: Optional[List[str]] = None
    variables: Optional[Dict[str, 'ConfigVariable']] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        result = {
            '__type': self.var_type.value,
            '__value': self.value
        }
        
        if self.var_type == VariableType.ENUM:
            result['__enumClass'] = self.enum_class
            result['__enumValues'] = self.enum_values
        elif self.var_type == VariableType.CUSTOM:
            if self.variables:
                result['__value'] = {
                    key: var.to_dict() for key, var in self.variables.items()
                }
            else:
                result['__value'] = None
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConfigVariable':
        """Create a ConfigVariable from a dictionary."""
        var_type = VariableType(data['__type'])
        value = data.get('__value')
        
        if var_type == VariableType.CUSTOM and value:
            variables = {
                key: cls.from_dict(var_data)
                for key, var_data in value.items()
            }
            return cls(
                var_type=var_type,
                value=value,
                variables=variables
            )
        elif var_type == VariableType.ENUM:
            return cls(
                var_type=var_type,
                value=value,
                enum_class=data.get('__enumClass'),
                enum_values=data.get('__enumValues')
            )
        else:
            return cls(var_type=var_type, value=value)
    
    @staticmethod
    def create_basic(value: Union[bool, int, float, str]) -> 'ConfigVariable':
        """Create a basic configuration variable from a Python value."""
        if isinstance(value, bool):
            var_type = VariableType.BOOLEAN
        elif isinstance(value, int):
            var_type = VariableType.INT
        elif isinstance(value, float):
            var_type = VariableType.DOUBLE
        elif isinstance(value, str):
            var_type = VariableType.STRING
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")
        
        return ConfigVariable(var_type=var_type, value=value)
    
    @staticmethod
    def create_custom(variables: Dict[str, 'ConfigVariable']) -> 'ConfigVariable':
        """Create a custom (nested) configuration variable."""
        return ConfigVariable(
            var_type=VariableType.CUSTOM,
            value=variables,
            variables=variables
        )


@dataclass
class RobotStatus:
    """Robot status information."""
    enabled: bool
    available: bool
    op_mode_name: str
    op_mode_status: str
    error_message: str
    warning_message: str
    battery_voltage: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RobotStatus':
        """Create a RobotStatus from a dictionary."""
        return cls(
            enabled=data.get('enabled', False),
            available=data.get('available', False),
            op_mode_name=data.get('opModeName', ''),
            op_mode_status=data.get('opModeStatus', ''),
            error_message=data.get('errorMessage', ''),
            warning_message=data.get('warningMessage', ''),
            battery_voltage=data.get('batteryVoltage', 0.0)
        )
