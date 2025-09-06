"""
digital_twin.py
Full city-scale simulation for NanoSploit (future module)
"""

import json
import random
import logging
from typing import Dict, List, Any
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class CityAsset:
    def __init__(self, asset_id: str, asset_type: str, properties: Dict[str, Any]):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.properties = properties
        self.status = "operational"
        self.compromised = False
        self.log = []

    def apply_attack(self, attack_type: str, params: Dict[str, Any]):
        # Simulate attack impact based on asset type
        impact = random.uniform(0, 1)
        self.compromised = impact > 0.7
        self.status = "compromised" if self.compromised else "operational"
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "attack_type": attack_type,
            "impact": impact,
            "status": self.status
        }
        self.log.append(entry)
        logging.info(f"Asset {self.asset_id} attacked: {entry}")
        return entry

    def recover(self):
        self.compromised = False
        self.status = "operational"
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "recover",
            "status": self.status
        }
        self.log.append(entry)
        logging.info(f"Asset {self.asset_id} recovered: {entry}")
        return entry

class DigitalTwin:
    def __init__(self, city_name: str):
        self.city_name = city_name
        self.assets: Dict[str, CityAsset] = {}
        self.scenarios: List[Dict[str, Any]] = []
        self.simulation_log: List[Dict[str, Any]] = []

    def add_asset(self, asset_id: str, asset_type: str, properties: Dict[str, Any]):
        asset = CityAsset(asset_id, asset_type, properties)
        self.assets[asset_id] = asset
        logging.info(f"Added asset {asset_id} of type {asset_type}")

    def load_scenario(self, scenario_file: str):
        with open(scenario_file, "r") as f:
            scenario = json.load(f)
        self.scenarios.append(scenario)
        logging.info(f"Loaded scenario: {scenario.get('name', 'Unnamed')}")
        return scenario

    def run_scenario(self, scenario: Dict[str, Any]):
        results = []
        for step in scenario.get("steps", []):
            asset_id = step["target_asset"]
            attack_type = step["attack_type"]
            params = step.get("params", {})
            asset = self.assets.get(asset_id)
            if asset:
                result = asset.apply_attack(attack_type, params)
                results.append(result)
            else:
                logging.warning(f"Asset {asset_id} not found in city model.")
        self.simulation_log.append({
            "scenario": scenario.get("name", "Unnamed"),
            "results": results
        })
        return results

    def get_asset_status(self):
        return {aid: asset.status for aid, asset in self.assets.items()}

    def get_compromised_assets(self):
        return [aid for aid, asset in self.assets.items() if asset.compromised]

    def recover_all(self):
        for asset in self.assets.values():
            asset.recover()
        logging.info("All assets recovered.")

    def generate_report(self):
        report = {
            "city": self.city_name,
            "timestamp": datetime.utcnow().isoformat(),
            "assets": {aid: {
                "type": asset.asset_type,
                "status": asset.status,
                "compromised": asset.compromised,
                "log": asset.log
            } for aid, asset in self.assets.items()},
            "scenarios": self.scenarios,
            "simulation_log": self.simulation_log
        }
        logging.info(f"Generated city-scale simulation report.")
        return report

    def save_report(self, path: str):
        report = self.generate_report()
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        logging.info(f"Report saved to {path}")

# Example usage (for testing/future integration)
if __name__ == "__main__":
    dt = DigitalTwin("Metropolis")
    dt.add_asset("traffic_light_1", "traffic_light", {"location": "Main & 1st"})
    dt.add_asset("cctv_1", "cctv", {"location": "Central Square"})
    dt.add_asset("grid_node_1", "power_grid", {"location": "Substation A"})
    scenario = {
        "name": "Smart City Blackout",
        "steps": [
            {"target_asset": "grid_node_1", "attack_type": "grid_overload", "params": {"level": "high"}},
            {"target_asset": "traffic_light_1", "attack_type": "signal_jam", "params": {"duration": 120}},
            {"target_asset": "cctv_1", "attack_type": "camera_blind", "params": {"method": "IR"}}
        ]
    }
    dt.scenarios.append(scenario)
    dt.run_scenario(scenario)
    dt.save_report("city_sim_report.json")
    print(json.dumps(dt.generate_report(), indent=2))
