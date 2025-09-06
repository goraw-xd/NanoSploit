import pytest
from nanosploit.core.protocol_abuse import ProtocolAbuseSimulator

def test_mqtt_flood():
    pas = ProtocolAbuseSimulator()
    result = pas.simulate('mqtt', '192.168.1.10', 'flood')
    assert 'success' in result or 'error' in result

def test_zigbee_replay():
    pas = ProtocolAbuseSimulator()
    result = pas.simulate('zigbee', 'zigbee-coordinator', 'replay')
    assert isinstance(result, dict)
