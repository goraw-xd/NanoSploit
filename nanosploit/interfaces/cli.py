"""
cli.py
Command-line interface for NanoSploit.
"""

import argparse
import sys
import os
import importlib
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Dynamic import helpers
def dynamic_import(module_path, class_name):
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except Exception as e:
        logging.error(f"Failed to import {class_name} from {module_path}: {e}")
        return None

# CLI core
class NanoSploitCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="NanoSploit CLI - Control & Visibility for IoT/Embedded Exploit Operations"
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self._register_core_commands()
        self._register_module_commands()
        self._register_ops_commands()
        self._register_reporting_commands()

    def _register_core_commands(self):
        core_parser = self.subparsers.add_parser("core", help="Core engine operations")
        core_sub = core_parser.add_subparsers(dest="core_cmd", required=True)

        # Payload Generator
        pg_parser = core_sub.add_parser("payload", help="Generate exploits for ARM/RISC-V/MIPS")
        pg_parser.add_argument("arch", choices=["arm", "riscv", "mips"], help="Target architecture")
        pg_parser.add_argument("output", help="Output file for payload")
        pg_parser.add_argument("--obfuscate", action="store_true", help="Enable XOR/ROP obfuscation")
        pg_parser.set_defaults(func=self.handle_payload)

        # Firmware Fuzzer
        ff_parser = core_sub.add_parser("fuzz", help="Fuzz firmware images")
        ff_parser.add_argument("firmware", help="Path to firmware image")
        ff_parser.add_argument("--auto-harness", action="store_true", help="Auto-generate fuzz harness")
        ff_parser.set_defaults(func=self.handle_fuzz)

        # Protocol Abuse
        pa_parser = core_sub.add_parser("protocol", help="Simulate protocol abuse attacks")
        pa_parser.add_argument("protocol", choices=["mqtt", "zigbee", "ble", "modbus", "can"], help="Protocol type")
        pa_parser.add_argument("target", help="Target device/IP")
        pa_parser.add_argument("--attack", required=True, help="Attack type (e.g., flood, injection)")
        pa_parser.set_defaults(func=self.handle_protocol)

        # HIL Emulator
        hil_parser = core_sub.add_parser("hil", help="Run payloads in QEMU/FPGA sandbox")
        hil_parser.add_argument("payload", help="Payload file")
        hil_parser.add_argument("chip", help="Chip type (e.g., cortex-m, fpga)")
        hil_parser.set_defaults(func=self.handle_hil)

        # Vuln Predictor
        vp_parser = core_sub.add_parser("predict", help="Predict vulnerabilities with ML")
        vp_parser.add_argument("firmware", help="Firmware image")
        vp_parser.set_defaults(func=self.handle_predict)

    def _register_module_commands(self):
        mod_parser = self.subparsers.add_parser("module", help="Specialized exploit modules")
        mod_sub = mod_parser.add_subparsers(dest="mod_cmd", required=True)
        for mod_name in ["medical_iot", "smart_city", "automotive", "consumer_iot", "industrial_iot"]:
            m_parser = mod_sub.add_parser(mod_name, help=f"Run {mod_name.replace('_', ' ').title()} module")
            m_parser.add_argument("action", choices=["scan", "exploit", "report"], help="Module action")
            m_parser.add_argument("target", help="Target device/IP")
            m_parser.add_argument("--params", help="Extra parameters (JSON)")
            m_parser.set_defaults(func=self.handle_module)

    def _register_ops_commands(self):
        ops_parser = self.subparsers.add_parser("ops", help="Red-team simulation layer")
        ops_sub = ops_parser.add_subparsers(dest="ops_cmd", required=True)

        # Scenario Builder
        sb_parser = ops_sub.add_parser("scenario", help="Build and run test scenarios")
        sb_parser.add_argument("scenario_file", help="Scenario JSON file")
        sb_parser.add_argument("--run", action="store_true", help="Run scenario after building")
        sb_parser.set_defaults(func=self.handle_scenario)

        # Attack Replay
        ar_parser = ops_sub.add_parser("replay", help="Replay exploit chains")
        ar_parser.add_argument("chain_file", help="Exploit chain JSON file")
        ar_parser.set_defaults(func=self.handle_replay)

        # Blue Team Sim
        bt_parser = ops_sub.add_parser("blueteam", help="Run blue-team defense drills")
        bt_parser.add_argument("drill_file", help="Drill JSON file")
        bt_parser.add_argument("--report", help="Output report file")
        bt_parser.set_defaults(func=self.handle_blueteam)

    def _register_reporting_commands(self):
        rep_parser = self.subparsers.add_parser("report", help="Reporting and visibility tools")
        rep_parser.add_argument("type", choices=["json", "log", "summary"], help="Report type")
        rep_parser.add_argument("source", help="Source file (scenario, drill, exploit)")
        rep_parser.set_defaults(func=self.handle_report)

    def run(self):
        args = self.parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            self.parser.print_help()

    # Core Handlers
    def handle_payload(self, args):
        PayloadGenerator = dynamic_import("nanosploit.core.payload_generator", "PayloadGenerator")
        if not PayloadGenerator:
            return
        pg = PayloadGenerator()
        payload = pg.generate(args.arch, obfuscate=args.obfuscate)
        with open(args.output, "wb") as f:
            f.write(payload)
        logging.info(f"Payload generated for {args.arch} and saved to {args.output}")

    def handle_fuzz(self, args):
        FirmwareFuzzer = dynamic_import("nanosploit.core.firmware_fuzzer", "FirmwareFuzzer")
        if not FirmwareFuzzer:
            return
        ff = FirmwareFuzzer()
        results = ff.fuzz(args.firmware, auto_harness=args.auto_harness)
        logging.info(f"Fuzzing results: {json.dumps(results, indent=2)}")

    def handle_protocol(self, args):
        ProtocolAbuseSimulator = dynamic_import("nanosploit.core.protocol_abuse", "ProtocolAbuseSimulator")
        if not ProtocolAbuseSimulator:
            return
        pas = ProtocolAbuseSimulator()
        result = pas.simulate(args.protocol, args.target, args.attack)
        logging.info(f"Protocol abuse result: {json.dumps(result, indent=2)}")

    def handle_hil(self, args):
        HILEmulator = dynamic_import("nanosploit.core.hil_emulator", "HILEmulator")
        if not HILEmulator:
            return
        hil = HILEmulator()
        score = hil.run(args.payload, args.chip)
        logging.info(f"HIL emulation complete. Pre-brick risk score: {score}")

    def handle_predict(self, args):
        VulnPredictor = dynamic_import("nanosploit.core.vuln_predictor", "VulnPredictor")
        if not VulnPredictor:
            return
        vp = VulnPredictor()
        prediction = vp.predict(args.firmware)
        logging.info(f"Vulnerability prediction: {json.dumps(prediction, indent=2)}")

    # Module Handler
    def handle_module(self, args):
        mod_map = {
            "medical_iot": ("nanosploit.modules.medical_iot", "MedicalIoTModule"),
            "smart_city": ("nanosploit.modules.smart_city", "SmartCityModule"),
            "automotive": ("nanosploit.modules.automotive", "AutomotiveModule"),
            "consumer_iot": ("nanosploit.modules.consumer_iot", "ConsumerIoTModule"),
            "industrial_iot": ("nanosploit.modules.industrial_iot", "IndustrialIoTModule"),
        }
        module_path, class_name = mod_map[args.mod_cmd]
        ModuleClass = dynamic_import(module_path, class_name)
        if not ModuleClass:
            return
        mod = ModuleClass()
        params = json.loads(args.params) if args.params else {}
        if args.action == "scan":
            result = mod.scan(args.target, **params)
        elif args.action == "exploit":
            result = mod.exploit(args.target, **params)
        elif args.action == "report":
            result = mod.report(args.target, **params)
        else:
            result = {"error": "Unknown action"}
        logging.info(f"Module {args.mod_cmd} {args.action} result: {json.dumps(result, indent=2)}")

    # Ops Handlers
    def handle_scenario(self, args):
        ScenarioBuilder = dynamic_import("nanosploit.ops.scenario_builder", "ScenarioBuilder")
        if not ScenarioBuilder:
            return
        sb = ScenarioBuilder()
        scenario = sb.load(args.scenario_file)
        logging.info(f"Scenario loaded: {json.dumps(scenario, indent=2)}")
        if args.run:
            results = sb.run(scenario)
            logging.info(f"Scenario run results: {json.dumps(results, indent=2)}")

    def handle_replay(self, args):
        AttackReplay = dynamic_import("nanosploit.ops.attack_replay", "AttackReplay")
        if not AttackReplay:
            return
        ar = AttackReplay()
        chain = ar.load(args.chain_file)
        results = ar.replay(chain)
        logging.info(f"Attack replay results: {json.dumps(results, indent=2)}")

    def handle_blueteam(self, args):
        BlueTeamSim = dynamic_import("nanosploit.ops.blueteam_sim", "BlueTeamSim")
        if not BlueTeamSim:
            return
        bt = BlueTeamSim()
        drill = bt.load_drill(args.drill_file)
        report = bt.run_drill(drill)
        logging.info(f"Blue-team drill report: {json.dumps(report, indent=2)}")
        if args.report:
            with open(args.report, "w") as f:
                json.dump(report, f, indent=2)
            logging.info(f"Drill report saved to {args.report}")

    # Reporting Handler
    def handle_report(self, args):
        try:
            with open(args.source, "r") as f:
                data = json.load(f)
            if args.type == "json":
                print(json.dumps(data, indent=2))
            elif args.type == "log":
                for entry in data.get("log", []):
                    print(f"[{entry['timestamp']}] {entry['level']}: {entry['message']}")
            elif args.type == "summary":
                summary = data.get("summary", "No summary available.")
                print(f"Summary: {summary}")
            else:
                print("Unknown report type.")
        except Exception as e:
            logging.error(f"Failed to generate report: {e}")

if __name__ == "__main__":
    NanoSploitCLI().run()
