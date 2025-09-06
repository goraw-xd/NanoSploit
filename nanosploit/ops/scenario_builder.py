"""
scenario_builder.py
Build and manage red-team test scenarios for NanoSploit.
"""

import logging
import json
import os
from typing import Dict, Any, List

class ScenarioBuilder:
    """
    Build and manage red-team test scenarios, including multi-stage attacks, device chains, and automated simulation plans.
    Supports scenario definition, validation, execution planning, and reporting.
    """
    def __init__(self, scenario_config: Dict[str, Any] = None):
        self.scenario_config = scenario_config or {}
        self.scenario_name = self.scenario_config.get("name", "UnnamedScenario")
        self.devices = self.scenario_config.get("devices", [])
        self.attack_chain = self.scenario_config.get("attack_chain", [])
        self.log_file = f"scenario_{self.scenario_name.replace(' ', '_')}.log"
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def define_scenario(self, name: str, devices: List[Dict[str, Any]], attack_chain: List[Dict[str, Any]]):
        """
        Define a new scenario with devices and attack chain.
        Args:
            name (str): Scenario name.
            devices (list): List of device profiles.
            attack_chain (list): List of attack steps.
        """
        self.scenario_name = name
        self.devices = devices
        self.attack_chain = attack_chain
        self.scenario_config = {
            "name": name,
            "devices": devices,
            "attack_chain": attack_chain
        }
        logging.info(f"Defined scenario: {self.scenario_config}")

    def validate_scenario(self) -> bool:
        """
        Validate the scenario configuration for completeness and logic.
        Returns:
            bool: True if valid, False otherwise.
        """
        if not self.scenario_name or not self.devices or not self.attack_chain:
            logging.error("Scenario validation failed: missing name, devices, or attack_chain.")
            return False
        # Example: check for duplicate device names
        device_names = [d.get("name") for d in self.devices]
        if len(device_names) != len(set(device_names)):
            logging.error("Scenario validation failed: duplicate device names.")
            return False
        logging.info("Scenario validated successfully.")
        return True

    def build_execution_plan(self) -> List[Dict[str, Any]]:
        """
        Build an execution plan for the scenario, mapping attack steps to devices.
        Returns:
            list: List of execution steps.
        """
        plan = []
        for step in self.attack_chain:
            device_name = step.get("device")
            device = next((d for d in self.devices if d.get("name") == device_name), None)
            if not device:
                logging.warning(f"Device {device_name} not found for step {step}")
                continue
            plan_step = {
                "device": device,
                "action": step.get("action"),
                "params": step.get("params", {})
            }
            plan.append(plan_step)
            logging.info(f"Added plan step: {plan_step}")
        return plan

    def simulate_scenario(self, plan: List[Dict[str, Any]], exploit_modules: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Simulate the scenario execution with real exploit module integration.
        Args:
            plan (list): Execution plan steps.
            exploit_modules (dict): Mapping of device types to exploit module instances.
        Returns:
            list: Simulation results for each step.
        """
        results = []
        for step in plan:
            device_type = step["device"].get("type", "generic")
            module = None
            if exploit_modules and device_type in exploit_modules:
                module = exploit_modules[device_type]
            # Prepare vulnerability and options
            vuln = step.get("params", {}).get("vuln")
            options = step.get("params", {}).get("options", {})
            if module and vuln:
                exploit = module.craft_exploit(vuln, options)
                sim_result = module.simulate_attack(exploit)
                result = {
                    "device": step["device"].get("name"),
                    "action": step["action"],
                    "params": step["params"],
                    "success": sim_result.get("success", False),
                    "impact": sim_result.get("impact", "N/A"),
                    "log": sim_result.get("log", "")
                }
            else:
                result = {
                    "device": step["device"].get("name"),
                    "action": step["action"],
                    "params": step["params"],
                    "success": True,  # fallback to mock
                    "impact": "Mock impact.",
                    "log": f"Simulated {step['action']} on {step['device'].get('name')} (mock)"
                }
            results.append(result)
            logging.info(f"Simulated scenario step: {result}")
        return results

    def automate_red_team_workflow(self, exploit_modules: Dict[str, Any] = None) -> str:
        """
        Automate the full red-team workflow: validate, plan, simulate, and report.
        Args:
            exploit_modules (dict): Mapping of device types to exploit module instances.
        Returns:
            str: Path to generated report.
        """
        if not self.validate_scenario():
            logging.error("Red-team workflow aborted: scenario invalid.")
            return ""
        plan = self.build_execution_plan()
        results = self.simulate_scenario(plan, exploit_modules)
        report_path = self.generate_report(results)
        logging.info(f"Automated red-team workflow completed. Report: {report_path}")
        return report_path

    def generate_report(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Generate a report of scenario simulation and save to JSON.
        Args:
            results (list): List of simulation results.
            output_path (str): Path to output JSON file.
        Returns:
            str: Path to saved report.
        """
        if not output_path:
            output_path = f"{self.scenario_name.replace(' ', '_')}_scenario_report.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        logging.info(f"Report generated at {output_path}")
        return output_path

    def get_logs(self) -> str:
        """
        Retrieve logs for this scenario builder.
        Returns:
            str: Log file contents.
        """
        if self.log_file and os.path.isfile(self.log_file):
            with open(self.log_file, "r") as f:
                return f.read()
        return ""
