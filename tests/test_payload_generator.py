import pytest
from nanosploit.core.payload_generator import PayloadGenerator

def test_generate_arm_payload():
    pg = PayloadGenerator()
    payload = pg.generate('arm', vendor='AcmeCorp', obfuscate=True, rop=True)
    assert isinstance(payload, bytes)
    assert len(payload) > 0

def test_generate_riscv_payload():
    pg = PayloadGenerator()
    payload = pg.generate('riscv', vendor='RiscVendor', obfuscate=False, rop=True)
    assert payload.startswith(b'\x7FRISCVHDR')

def test_xor_obfuscation_changes_payload():
    pg = PayloadGenerator()
    raw = b'1234567890'
    obfuscated = pg.xor_obfuscate(raw, key=42)
    assert obfuscated != raw
