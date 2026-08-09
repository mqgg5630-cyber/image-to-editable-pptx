from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_page_ir.py"
spec = importlib.util.spec_from_file_location("validate_page_ir", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class PageIRValidationTests(unittest.TestCase):
    def test_minimal_fixture_is_valid(self):
        path = ROOT / "examples" / "minimal" / "page_ir.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(module.validate_page_ir(payload, path.parent), [])

    def test_duplicate_object_id_is_rejected(self):
        payload = {
            "schema_version": "1.0",
            "pages": [
                {
                    "id": "slide-1",
                    "width_px": 100,
                    "height_px": 100,
                    "background": "#FFFFFF",
                    "objects": [
                        {"id": "x", "type": "rect", "bbox": [0, 0, 10, 10]},
                        {"id": "x", "type": "rect", "bbox": [20, 20, 10, 10]},
                    ],
                }
            ],
        }
        errors = module.validate_page_ir(payload, ROOT)
        self.assertTrue(any("duplicate object id" in item for item in errors))

    def test_out_of_bounds_is_rejected(self):
        payload = {
            "schema_version": "1.0",
            "pages": [
                {
                    "id": "slide-1",
                    "width_px": 100,
                    "height_px": 100,
                    "background": "#FFFFFF",
                    "objects": [{"id": "x", "type": "rect", "bbox": [90, 90, 20, 20]}],
                }
            ],
        }
        errors = module.validate_page_ir(payload, ROOT)
        self.assertTrue(any("outside the page" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
