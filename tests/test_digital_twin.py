import pytest
from nanosploit.future.digital_twin import DigitalTwin

def test_city_asset_add_and_attack():
    dt = DigitalTwin('Testopolis')
    dt.add_asset('traffic_light_1', 'traffic_light', {'location': 'Main & 1st'})
    scenario = {
        'name': 'TL Attack',
        'steps': [
            {'target_asset': 'traffic_light_1', 'attack_type': 'signal_jam', 'params': {'duration': 60}}
        ]
    }
    dt.scenarios.append(scenario)
    results = dt.run_scenario(scenario)
    assert any('attack_type' in r for r in results)
