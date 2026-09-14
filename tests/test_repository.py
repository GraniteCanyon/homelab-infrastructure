import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_inventory_is_explicitly_not_live(self):
        data = json.loads((ROOT / "examples/inventory.json").read_text())
        self.assertFalse(data["live_configuration"])
        self.assertEqual(data["kind"], "documentation-example")
        self.assertEqual({v["id"] for v in data["vlans"]}, {10, 20, 30, 40})
        self.assertEqual(len(data["vlans"]), 4)

    def test_policy_is_proposed(self):
        with (ROOT / "examples/policy-intent.csv").open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        self.assertTrue(all(r["status"] == "proposed-review-baseline" for r in rows))

    def test_relative_markdown_links(self):
        for path in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" not in link and not link.startswith("#"):
                    self.assertTrue((path.parent / link.split("#")[0]).exists(), (path, link))


if __name__ == "__main__":
    unittest.main()
