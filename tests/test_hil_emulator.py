import pytest
from nanosploit.core.hil_emulator import HILEmulator

def test_hil_run():
    hil = HILEmulator()
    score = hil.run('payload.bin', 'cortex-m')
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
