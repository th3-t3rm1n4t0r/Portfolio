from project import validate_target, scan_port, load_ports
from unittest.mock import patch
import pytest

def test_load_ports_missing_file():
    with pytest.raises(SystemExit):
        load_ports("Random data")

def test_load_ports_correct_file():
    ports = load_ports("services.csv")
    assert isinstance(ports, dict)
    assert len(ports) > 0

def test_validate_target_incorrect_input():
    with pytest.raises(SystemExit):
        validate_target("Incorrect URL")

def test_validate_target_correct_input():
    ip = validate_target("google.com")
    assert isinstance(ip, str)

@patch("project.socket.socket")
def test_scan_port_success(mock_socket):
    mock_inst = mock_socket.return_value
    mock_inst.connect_ex.return_value = 0
    result = scan_port(("127.0.0.1", 80))
    assert result == 0
    assert isinstance(result, int)
    mock_inst.settimeout.assert_called_with(1)

@patch("project.socket.socket")
def test_scan_port_closed(mock_socket):
    mock_inst = mock_socket.return_value
    mock_inst.connect_ex.return_value = 111
    result = scan_port(("127.0.0.1", 80))
    assert result == 111
    mock_inst.connect_ex.assert_called_once_with(("127.0.0.1", 80))