import csv
import tempfile
import unittest
from pathlib import Path

from ai_automation_lab.week02_safe_cleaner import (
    clean_column_name,
    clean_text,
    mask_email,
    mask_phone,
    clean_csv,
)


class TestWeek02SafeCleaner(unittest.TestCase):
    def test_clean_column_name(self):
        self.assertEqual(clean_column_name(" Full Name "), "full_name")
        self.assertEqual(clean_column_name("Email Address"), "email_address")
        self.assertEqual(clean_column_name("Phone-Number"), "phone_number")

    def test_clean_text(self):
        self.assertEqual(clean_text("  Anna   Petrova  "), "Anna Petrova")
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")

    def test_mask_email(self):
        self.assertEqual(mask_email("anna@example.com"), "a***@example.com")
        self.assertEqual(mask_email("x@test.com"), "***@test.com")
        self.assertEqual(mask_email("not-email"), "not-email")

    def test_mask_phone(self):
        self.assertEqual(mask_phone("+7 999 123-45-67"), "+7********67")
        self.assertEqual(mask_phone("89991234567"), "8********67")
        self.assertEqual(mask_phone("no phone"), "no phone")

    def test_clean_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "dirty.csv"
            output_path = Path(temp_dir) / "clean.csv"

            input_path.write_text(
                " Full Name , Email Address , Phone-Number , Budget USD \n"
                "  Anna   Petrova  , anna@example.com , +7 999 123-45-67 , 1000 \n"
                " , , , \n"
                " Ivan Ivanov , ivan@test.com , 89991234567 , 2000 \n",
                encoding="utf-8",
            )

            report = clean_csv(input_path, output_path)

            self.assertTrue(output_path.exists())
            self.assertEqual(report["input_rows"], 3)
            self.assertEqual(report["output_rows"], 2)
            self.assertEqual(report["masked_emails"], 2)
            self.assertEqual(report["masked_phones"], 2)

            with output_path.open("r", encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(rows[0]["full_name"], "Anna Petrova")
            self.assertEqual(rows[0]["email_address"], "a***@example.com")
            self.assertEqual(rows[0]["phone_number"], "+7********67")


if __name__ == "__main__":
    unittest.main()