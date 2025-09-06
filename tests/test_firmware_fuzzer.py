import pytest
from nanosploit.core.firmware_fuzzer import FirmwareFuzzer

def test_fuzz_firmware():
    ff = FirmwareFuzzer()
    results = ff.fuzz('firmware.bin', auto_harness=True)
    assert isinstance(results, dict)
    assert 'findings' in results or 'errors' in results
