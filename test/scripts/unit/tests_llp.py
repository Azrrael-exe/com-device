import pytest
from scripts.llp import LLParser

def test_ll_parser():
    parser = LLParser(header=0x7e)

    message = [0x7e, 0x03, 0x01, 0x00, 0x00, 0x00]

    with pytest.raises(AssertionError):
        parser.parse(message)

    payload = [0xA1, 0x00, 0x02, 0x0A2, 0x00, 0x01]
    message = [0x7e, 0x06] + payload + [(0xFF - sum(payload)) %256]

    parser.parse(message)

    payload = [0xA1, 0x00, 0x02, 0x0A2, 0x00, 0x01]
    message = [0x7e, 0x06] + payload + [(0xFF - sum(payload)) %256]

    parser.parse(message)

    assert parser.available() == 2
    assert len(parser.get_buffer()) == 2
    assert parser.available() == 0

    payload = {
        0x0A: 0xAB01,
        0x0B: 0xAB02,
        0x0C: 0xAB03,
        0x0D: 0xAB04,
        0x0E: 0xAB05,
        0x0F: 0xAB06,
    }

    parser.enconde(payload=payload)