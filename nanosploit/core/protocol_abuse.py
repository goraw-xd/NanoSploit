"""
protocol_abuse.py
Simulate protocol attacks (MQTT, Zigbee, BLE, Modbus, CAN).
"""

SUPPORTED_PROTOCOLS = ["mqtt", "zigbee", "ble", "modbus", "can"]

class ProtocolAbuseSimulator:
    def __init__(self, protocol):
        protocol = protocol.lower()
        if protocol not in SUPPORTED_PROTOCOLS:
            raise ValueError(f"Unsupported protocol: {protocol}. Supported: {SUPPORTED_PROTOCOLS}")
        self.protocol = protocol

    def attack(self, attack_type, target, options=None):
        """
        Simulate a protocol abuse attack.
        Args:
            attack_type (str): Type of attack (e.g., 'flood', 'replay', 'inject', etc.)
            target (str): Target device or endpoint.
            options (dict): Additional options for the attack.
        Returns:
            str: Result of the simulated attack (mocked).
        """
        if options is None:
            options = {}
        if self.protocol == "mqtt":
            return self._mqtt_attack(attack_type, target, options)
        elif self.protocol == "zigbee":
            return self._zigbee_attack(attack_type, target, options)
        elif self.protocol == "ble":
            return self._ble_attack(attack_type, target, options)
        elif self.protocol == "modbus":
            return self._modbus_attack(attack_type, target, options)
        elif self.protocol == "can":
            return self._can_attack(attack_type, target, options)
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

    def _mqtt_attack(self, attack_type, target, options):
        if attack_type == "flood":
            return f"[MOCK] MQTT message flood attack on broker {target}"
        elif attack_type == "poison":
            return f"[MOCK] MQTT broker poisoning on {target}"
        else:
            return f"[MOCK] MQTT attack '{attack_type}' on {target}"

    def _zigbee_attack(self, attack_type, target, options):
        if attack_type == "replay":
            return f"[MOCK] Zigbee replay attack on {target}"
        elif attack_type == "rogue_coordinator":
            return f"[MOCK] Zigbee rogue coordinator injection on {target}"
        else:
            return f"[MOCK] Zigbee attack '{attack_type}' on {target}"

    def _ble_attack(self, attack_type, target, options):
        if attack_type == "pairing_bypass":
            return f"[MOCK] BLE pairing bypass on {target}"
        elif attack_type == "dos":
            return f"[MOCK] BLE DoS via crafted L2CAP packets on {target}"
        else:
            return f"[MOCK] BLE attack '{attack_type}' on {target}"

    def _modbus_attack(self, attack_type, target, options):
        if attack_type == "command_injection":
            return f"[MOCK] Modbus command injection on PLC {target}"
        else:
            return f"[MOCK] Modbus attack '{attack_type}' on {target}"

    def _can_attack(self, attack_type, target, options):
        if attack_type == "malicious_frame":
            return f"[MOCK] CAN bus malicious frame sent to {target}"
        else:
            return f"[MOCK] CAN bus attack '{attack_type}' on {target}"
