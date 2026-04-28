import tempfile
import unittest
from pathlib import Path

from ai_automation_lab.main import build_summary, load_leads, save_json


class TestLeadSummary(unittest.TestCase):
    def test_build_summary(self):
        leads = [
            {"lead_id": "1", "budget_usd": "1000"},
            {"lead_id": "2", "budget_usd": "2500"},
            {"lead_id": "3", "budget_usd": "invalid"},
        ]

        result = build_summary(leads)

        self.assertEqual(result["total_leads"], 3)
        self.assertEqual(result["total_budget_usd"], 3500)

    def test_load_leads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "leads.csv"
            input_path.write_text(
                "lead_id,name,budget_usd\n"
                "1,Anna,1000\n"
                "2,Ivan,2000\n",
                encoding="utf-8",
            )

            leads = load_leads(input_path)

            self.assertEqual(len(leads), 2)
            self.assertEqual(leads[0]["name"], "Anna")

    def test_save_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "summary.json"

            save_json({"total_leads": 2, "total_budget_usd": 3000}, output_path)

            self.assertTrue(output_path.exists())
            self.assertIn("total_budget_usd", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
