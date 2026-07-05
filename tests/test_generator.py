import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generator import generate_code_from_definition


def test_generate_code_supports_list_fields():
    data_def = {
        "SensorData": {
            "sensor_id": "int",
            "samples": "list",
        }
    }

    generated_code = generate_code_from_definition(data_def)

    assert "def serialize(self):" in generated_code
    assert "samples" in generated_code
    assert "len(self.samples)" in generated_code
    assert "for item in self.samples" in generated_code
