"""
Basic tests for the FTC Dashboard Python client.

These tests verify the client structure and type conversions without
requiring a live dashboard server.
"""

import sys
sys.path.insert(0, '.')

from ftc_dashboard_client import (
    DashboardClient,
    TelemetryPacket,
    ConfigVariable,
    VariableType,
    RobotStatus
)


def test_telemetry_packet_from_dict():
    """Test TelemetryPacket creation from dictionary."""
    data = {
        'timestamp': 1234567890,
        'data': {'x': '1.5', 'y': '2.5'},
        'log': ['Test log message'],
        'field': {'ops': []},
        'fieldOverlay': {'ops': []}
    }
    
    packet = TelemetryPacket.from_dict(data)
    
    assert packet.timestamp == 1234567890
    assert packet.data['x'] == '1.5'
    assert packet.log[0] == 'Test log message'
    print("✓ TelemetryPacket.from_dict() works correctly")


def test_config_variable_basic():
    """Test basic ConfigVariable creation and conversion."""
    # Test integer
    var = ConfigVariable.create_basic(42)
    assert var.var_type == VariableType.INT
    assert var.value == 42
    
    var_dict = var.to_dict()
    assert var_dict['__type'] == 'int'
    assert var_dict['__value'] == 42
    
    # Test boolean
    var = ConfigVariable.create_basic(True)
    assert var.var_type == VariableType.BOOLEAN
    assert var.value == True
    
    # Test float
    var = ConfigVariable.create_basic(3.14)
    assert var.var_type == VariableType.DOUBLE
    assert var.value == 3.14
    
    # Test string
    var = ConfigVariable.create_basic("test")
    assert var.var_type == VariableType.STRING
    assert var.value == "test"
    
    print("✓ ConfigVariable.create_basic() works correctly")


def test_config_variable_custom():
    """Test custom (nested) ConfigVariable creation."""
    variables = {
        'speed': ConfigVariable.create_basic(1.5),
        'enabled': ConfigVariable.create_basic(True),
        'name': ConfigVariable.create_basic("robot")
    }
    
    custom_var = ConfigVariable.create_custom(variables)
    assert custom_var.var_type == VariableType.CUSTOM
    assert 'speed' in custom_var.variables
    assert 'enabled' in custom_var.variables
    
    var_dict = custom_var.to_dict()
    assert var_dict['__type'] == 'custom'
    assert '__value' in var_dict
    assert 'speed' in var_dict['__value']
    
    print("✓ ConfigVariable.create_custom() works correctly")


def test_config_variable_from_dict():
    """Test ConfigVariable deserialization from dictionary."""
    # Test basic variable
    data = {
        '__type': 'double',
        '__value': 1.5
    }
    var = ConfigVariable.from_dict(data)
    assert var.var_type == VariableType.DOUBLE
    assert var.value == 1.5
    
    # Test custom variable
    data = {
        '__type': 'custom',
        '__value': {
            'speed': {'__type': 'double', '__value': 2.5},
            'enabled': {'__type': 'boolean', '__value': True}
        }
    }
    var = ConfigVariable.from_dict(data)
    assert var.var_type == VariableType.CUSTOM
    assert 'speed' in var.variables
    assert var.variables['speed'].value == 2.5
    
    print("✓ ConfigVariable.from_dict() works correctly")


def test_robot_status_from_dict():
    """Test RobotStatus creation from dictionary."""
    data = {
        'enabled': True,
        'available': True,
        'opModeName': 'TestOpMode',
        'opModeStatus': 'RUNNING',
        'errorMessage': '',
        'warningMessage': '',
        'batteryVoltage': 12.5
    }
    
    status = RobotStatus.from_dict(data)
    assert status.enabled == True
    assert status.op_mode_name == 'TestOpMode'
    assert status.battery_voltage == 12.5
    
    print("✓ RobotStatus.from_dict() works correctly")


def test_dashboard_client_initialization():
    """Test DashboardClient initialization."""
    # Test default parameters
    client = DashboardClient()
    assert client.host == "192.168.49.1"
    assert client.port == 8000
    assert client.auto_reconnect == True
    assert client.connected == False
    
    # Test custom parameters
    client = DashboardClient(host="192.168.43.1", port=9000, auto_reconnect=False)
    assert client.host == "192.168.43.1"
    assert client.port == 9000
    assert client.auto_reconnect == False
    
    print("✓ DashboardClient initialization works correctly")


def test_message_types():
    """Test that all message types are defined."""
    from ftc_dashboard_client import MessageType
    
    assert MessageType.GET_ROBOT_STATUS.value == "GET_ROBOT_STATUS"
    assert MessageType.RECEIVE_TELEMETRY.value == "RECEIVE_TELEMETRY"
    assert MessageType.GET_CONFIG.value == "GET_CONFIG"
    assert MessageType.SAVE_CONFIG.value == "SAVE_CONFIG"
    assert MessageType.RECEIVE_CONFIG.value == "RECEIVE_CONFIG"
    
    print("✓ All MessageType constants are defined")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running FTC Dashboard Python Client Tests")
    print("=" * 60)
    print()
    
    test_telemetry_packet_from_dict()
    test_config_variable_basic()
    test_config_variable_custom()
    test_config_variable_from_dict()
    test_robot_status_from_dict()
    test_dashboard_client_initialization()
    test_message_types()
    
    print()
    print("=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
