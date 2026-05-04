import argparse
import csv
import json
import re
from pathlib import Path


def clean_column_name(name):
    if name is None:
        return ""

    cleaned = str(name).strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("_")

    return cleaned


def clean_text(value):
    if value is None:
        return ""

    return " ".join(str(value).strip().split())


def mask_email(value):
    cleaned = clean_text(value)

    if "@" not in cleaned:
        return cleaned

    local_part, domain = cleaned.split("@", 1)

    if not local_part or "." not in domain:
        return cleaned

    if len(local_part) == 1:
        return f"***@{domain}"

    return f"{local_part[0]}***@{domain}"


def mask_phone(value):
    cleaned = clean_text(value)
    digits = re.sub(r"\D", "", cleaned)

    if len(digits) < 7:
        return cleaned

    if cleaned.startswith("+"):
        prefix = f"+{digits[0]}"
    else:
        prefix = digits[0]

    suffix = digits[-2:]
    hidden_length = max(len(digits) - 3, 0)

    return f"{prefix}{'*' * hidden_length}{suffix}"


def clean_csv(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        original_columns = reader.fieldnames or []
        cleaned_columns = [clean_column_name(column) for column in original_columns]
        raw_rows = list(reader)

    report = {
        "input_rows": len(raw_rows),
        "output_rows": 0,
        "masked_emails": 0,
        "masked_phones": 0,
    }

    cleaned_rows = []

    for raw_row in raw_rows:
        cleaned_row = {}

        for original_column, cleaned_column in zip(original_columns, cleaned_columns):
            value = clean_text(raw_row.get(original_column, ""))

            if "email" in cleaned_column:
                masked_value = mask_email(value)

                if masked_value != value:
                    report["masked_emails"] += 1

                value = masked_value

            if "phone" in cleaned_column or "tel" in cleaned_column:
                masked_value = mask_phone(value)

                if masked_value != value:
                    report["masked_phones"] += 1

                value = masked_value

            cleaned_row[cleaned_column] = value

        if any(value != "" for value in cleaned_row.values()):
            cleaned_rows.append(cleaned_row)

    report["output_rows"] = len(cleaned_rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=cleaned_columns)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    return report


def save_report(report, report_path):
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="Week 02 safe CSV data cleaner")
    parser.add_argument("--input", required=True, help="Path to dirty input CSV")
    parser.add_argument("--output", required=True, help="Path to cleaned output CSV")
    parser.add_argument("--report", required=False, help="Path to JSON cleaning report")

    args = parser.parse_args()

    report = clean_csv(args.input, args.output)

    if args.report:
        save_report(report, args.report)

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()