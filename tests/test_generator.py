import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from generator import generate_code_from_definition


class GeneratorTests(unittest.TestCase):
    def test_generate_code_supports_list_fields(self):
        data_def = {
            "SensorData": {
                "sensor_id": "int",
                "samples": "list",
            }
        }

        generated_code = generate_code_from_definition(data_def)

        self.assertIn("def serialize(self):", generated_code)
        self.assertIn("samples", generated_code)
        self.assertIn("len(self.samples)", generated_code)
        self.assertIn("for item in self.samples", generated_code)

    def test_invalid_field_type_raises_value_error(self):
        data_def = {
            "SensorData": {
                "value": "unknown",
            }
        }

        with self.assertRaises(ValueError):
            generate_code_from_definition(data_def)


if __name__ == "__main__":
    unittest.main()
