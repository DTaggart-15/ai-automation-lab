import json
import tempfile
import unittest
from pathlib import Path

from ai_automation_lab.week02_safe_cleaner import (
    build_summary,
    clean_row,
    load_rows,
    process_rows,
    write_csv,
    write_json,
)


class TestWeek02SafeCleaner(unittest.TestCase):
    def test_clean_row_returns_safe_record(self):
        row = {
            "lead_ref": "LD-0001",
            "contact_alias": "contact_001",
            "contact_email": "contact_001@example.com",
            "company_alias": "org_alpha",
            "requested_service": "invoice_automation",
            "budget_usd": "5000.00",
            "requested_due_date": "2026-05-15",
            "country_code": "GB",
        }

        cleaned, error = clean_row(2, row)

        self.assertIsNone(error)
        self.assertIsNotNone(cleaned)
        self.assertEqual(cleaned["lead_ref"], "LD-0001")
        self.assertEqual(cleaned["priority"], "normal")
        self.assertNotIn("contact_email", cleaned)

    def test_clean_row_rejects_non_demo_domain(self):
        row = {
            "lead_ref": "LD-0002",
            "contact_alias": "contact_002",
            "contact_email": "contact_002@example.net",
            "company_alias": "org_beta",
            "requested_service": "support_triage",
            "budget_usd": "8200.50",
            "requested_due_date": "2026-05-20",
            "country_code": "DE",
        }

        cleaned, error = clean_row(3, row)

        self.assertIsNone(cleaned)
        self.assertIsNotNone(error)

        fields = {item["field"] for item in error["errors"]}

        self.assertIn("contact_email", fields)

    def test_end_to_end_outputs(self):
        csv_content = (
            "lead_ref,contact_alias,contact_email,company_alias,requested_service,"
            "budget_usd,requested_due_date,country_code\n"
            "LD-0001,contact_001,contact_001@example.com,org_alpha,invoice_automation,"
            "5000.00,2026-05-15,GB\n"
            "LD-0002,contact_002,contact_002@example.net,org_beta,support_triage,"
            "8200.50,2026-05-20,DE\n"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "leads.csv"
            output_dir = temp_path / "out"

            input_path.write_text(csv_content, encoding="utf-8")

            rows = load_rows(input_path)
            cleaned_rows, error_rows = process_rows(rows)
            summary = build_summary(cleaned_rows, error_rows, len(rows))

            write_csv(cleaned_rows, output_dir / "cleaned_leads.csv")
            write_json(cleaned_rows, output_dir / "cleaned_leads.json")
            write_json(error_rows, output_dir / "errors.json")
            write_json(summary, output_dir / "summary.json")

            self.assertTrue((output_dir / "cleaned_leads.csv").exists())
            self.assertTrue((output_dir / "cleaned_leads.json").exists())
            self.assertTrue((output_dir / "errors.json").exists())
            self.assertTrue((output_dir / "summary.json").exists())

            loaded_summary = json.loads(
                (output_dir / "summary.json").read_text(encoding="utf-8")
            )

            self.assertEqual(loaded_summary["total_rows"], 2)
            self.assertEqual(loaded_summary["valid_rows"], 1)
            self.assertEqual(loaded_summary["invalid_rows"], 1)
            self.assertEqual(loaded_summary["total_valid_budget_usd"], "5000.00")


if __name__ == "__main__":
    unittest.main()