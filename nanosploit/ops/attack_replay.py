"""
attack_replay.py
Replay exploit chains for red-team operations in NanoSploit.
"""

import logging
import json
import os
from typing import Dict, Any, List

class AttackReplay:
    """
    Replay exploit chains for red-team operations, including multi-stage attacks, scenario replays, and result analysis.
    Supports loading replay data, executing chains, tracking outcomes, and generating reports.
    """
    def __init__(self, replay_config: Dict[str, Any] = None):
        self.replay_config = replay_config or {}
        self.chain_name = self.replay_config.get("name", "UnnamedChain")
        self.chain_steps = self.replay_config.get("chain_steps", [])
        self.log_file = f"attack_replay_{self.chain_name.replace(' ', '_')}.log"
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def load_chain(self, chain_path: str):
        """
        Load an exploit chain from a JSON file.
        Args:
            chain_path (str): Path to chain JSON file.
        """
        if not os.path.isfile(chain_path):
            logging.error(f"Chain file not found: {chain_path}")
            return False
        with open(chain_path, "r") as f:
            data = json.load(f)
        self.chain_name = data.get("name", "UnnamedChain")
        self.chain_steps = data.get("chain_steps", [])
        self.replay_config = data
        logging.info(f"Loaded chain: {self.chain_name} with {len(self.chain_steps)} steps.")
        return True

    def replay_chain(self, exploit_modules: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Replay the loaded exploit chain using provided exploit modules.
        Args:
            exploit_modules (dict): Mapping of device types to exploit module instances.
        Returns:
            list: Results for each chain step.
        """
        results = []
        for step in self.chain_steps:
            device_type = step.get("device_type", "generic")
            module = None
            if exploit_modules and device_type in exploit_modules:
                module = exploit_modules[device_type]
            vuln = step.get("vuln")
            options = step.get("options", {})
            if module and vuln:
                exploit = module.craft_exploit(vuln, options)
                sim_result = module.simulate_attack(exploit)
                result = {
                    "device": step.get("device_name", "unknown"),
                    "action": step.get("action", "unknown"),
                    "success": sim_result.get("success", False),
                    "impact": sim_result.get("impact", "N/A"),
                    "log": sim_result.get("log", "")
                }
            else:
                result = {
                    "device": step.get("device_name", "unknown"),
                    "action": step.get("action", "unknown"),
                    "success": True,  # fallback to mock
                    "impact": "Mock impact.",
                    "log": f"Replayed {step.get('action', 'unknown')} on {step.get('device_name', 'unknown')} (mock)"
                }
            results.append(result)
            logging.info(f"Replayed chain step: {result}")
        return results

    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the results of the replayed chain for success, failure, and impact.
        Args:
            results (list): List of chain step results.
        Returns:
            dict: Analysis summary.
        """
        total = len(results)
        successes = sum(1 for r in results if r["success"])
        failures = total - successes
        impacts = [r["impact"] for r in results]
        summary = {
            "chain_name": self.chain_name,
            "total_steps": total,
            "successes": successes,
            "failures": failures,
            "impacts": impacts,
            "overall_success": successes == total
        }
        logging.info(f"Chain analysis summary: {summary}")
        return summary

    def generate_report(self, results: List[Dict[str, Any]], summary: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate a report of chain replay and analysis, save to JSON.
        Args:
            results (list): List of chain step results.
            summary (dict): Analysis summary.
            output_path (str): Path to output JSON file.
        Returns:
            str: Path to saved report.
        """
        report = {
            "chain_name": self.chain_name,
            "results": results,
            "summary": summary
        }
        if not output_path:
            output_path = f"{self.chain_name.replace(' ', '_')}_attackreplay_report.json"
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        logging.info(f"Report generated at {output_path}")
        return output_path

    def get_logs(self) -> str:
        """
        Retrieve logs for this attack replay module.
        Returns:
            str: Log file contents.
        """
        if self.log_file and os.path.isfile(self.log_file):
            with open(self.log_file, "r") as f:
                return f.read()
        return ""

    def automate_chain_replay(self, chain_path: str, exploit_modules: Dict[str, Any] = None) -> str:
        """
        Automate the full replay and analysis of a multi-stage exploit chain.
        Args:
            chain_path (str): Path to chain JSON file.
            exploit_modules (dict): Mapping of device types to exploit module instances.
        Returns:
            str: Path to generated report.
        """
        if not self.load_chain(chain_path):
            logging.error("Automated chain replay aborted: chain file not found or invalid.")
            return ""
        results = self.replay_chain(exploit_modules)
        summary = self.analyze_results(results)
        report_path = self.generate_report(results, summary)
        logging.info(f"Automated chain replay completed. Report: {report_path}")
        return report_path
