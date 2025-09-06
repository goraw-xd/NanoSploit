"""
blueteam_sim.py
Blue-team defense simulation and drills for NanoSploit.
"""

import logging
import json
import os
from typing import Dict, Any, List

class BlueTeamSim:
    """
    Simulate blue-team defense drills, including detection, response, and mitigation of red-team scenarios.
    Supports scenario loading, defense strategy planning, incident simulation, and reporting.
    """
    def __init__(self, drill_config: Dict[str, Any] = None):
        self.drill_config = drill_config or {}
        self.scenario_name = self.drill_config.get("scenario_name", "UnnamedDrill")
        self.incidents = self.drill_config.get("incidents", [])
        self.defense_strategies = self.drill_config.get("defense_strategies", [])
        self.log_file = f"blueteam_sim_{self.scenario_name.replace(' ', '_')}.log"
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def load_drill(self, drill_path: str):
        """
        Load a blue-team drill scenario from a JSON file.
        Args:
            drill_path (str): Path to drill JSON file.
        """
        if not os.path.isfile(drill_path):
            logging.error(f"Drill file not found: {drill_path}")
            return False
        with open(drill_path, "r") as f:
            data = json.load(f)
        self.scenario_name = data.get("scenario_name", "UnnamedDrill")
        self.incidents = data.get("incidents", [])
        self.defense_strategies = data.get("defense_strategies", [])
        self.drill_config = data
        logging.info(f"Loaded drill: {self.scenario_name} with {len(self.incidents)} incidents.")
        return True

    def plan_defense(self) -> List[Dict[str, Any]]:
        """
        Plan defense strategies for each incident in the drill.
        Returns:
            list: List of defense plans for each incident.
        """
        plans = []
        for incident in self.incidents:
            strategy = self._select_strategy(incident)
            plan = {
                "incident": incident,
                "strategy": strategy,
                "log": f"Planned defense for incident {incident.get('type', 'unknown')}"
            }
            plans.append(plan)
            logging.info(f"Defense plan: {plan}")
        return plans

    def _select_strategy(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select an appropriate defense strategy for a given incident.
        Args:
            incident (dict): Incident details.
        Returns:
            dict: Selected strategy.
        """
        # Mock logic: select first matching strategy or fallback
        for strategy in self.defense_strategies:
            if strategy.get("incident_type") == incident.get("type"):
                return strategy
        return {"incident_type": incident.get("type"), "action": "isolate_device", "description": "Default: Isolate affected device."}

    def simulate_defense(self, plans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simulate blue-team defense actions for each incident.
        Args:
            plans (list): List of defense plans.
        Returns:
            list: Simulation results for each defense action.
        """
        results = []
        for plan in plans:
            incident = plan["incident"]
            strategy = plan["strategy"]
            success = self._simulate_action(incident, strategy)
            result = {
                "incident": incident,
                "strategy": strategy,
                "success": success,
                "log": f"Simulated defense action {strategy.get('action', 'unknown')} for incident {incident.get('type', 'unknown')}"
            }
            results.append(result)
            logging.info(f"Simulated defense result: {result}")
        return results

    def _simulate_action(self, incident: Dict[str, Any], strategy: Dict[str, Any]) -> bool:
        """
        Simulate the outcome of a defense action (mocked logic).
        Args:
            incident (dict): Incident details.
            strategy (dict): Defense strategy.
        Returns:
            bool: True if defense is successful, False otherwise.
        """
        # Mock: randomize success based on incident severity
        severity = incident.get("severity", "medium")
        if severity == "critical":
            return strategy.get("action") in ["isolate_device", "shutdown_network"]
        elif severity == "high":
            return strategy.get("action") in ["isolate_device", "patch_firmware"]
        else:
            return True

    def generate_report(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Generate a report of defense simulation and save to JSON.
        Args:
            results (list): List of defense simulation results.
            output_path (str): Path to output JSON file.
        Returns:
            str: Path to saved report.
        """
        report = {
            "scenario_name": self.scenario_name,
            "defense_results": results
        }
        if not output_path:
            output_path = f"{self.scenario_name.replace(' ', '_')}_blueteam_report.json"
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        logging.info(f"Report generated at {output_path}")
        return output_path

    def get_logs(self) -> str:
        """
        Retrieve logs for this blue-team simulation module.
        Returns:
            str: Log file contents.
        """
        if self.log_file and os.path.isfile(self.log_file):
            with open(self.log_file, "r") as f:
                return f.read()
        return ""
