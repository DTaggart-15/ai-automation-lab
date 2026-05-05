from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)

ALLOWED_DEMO_DOMAINS = {"example.com", "example.org"}

LEAD_REF_RE = re.compile(r"^LD-\d{4}$")
ALIAS_RE = re.compile(r"^[a-z0-9_]{3,40}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,63}$")
SERVICE_RE = re.compile(r"^[a-z0-9_]{3,50}$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")

SAFE_FIELDNAMES = [
    "lead_ref",
    "contact_alias",
    "company_alias",
    "requested_service",
    "budget_usd",
    "requested_due_date",
    "country_code",
    "priority",
]


def raw_value(row: dict[str, Any], key: str) -> str:
    value = row.get(key, "")

    if value is None:
        return ""

    return str(value)


def normalize_token(value: str) -> str:
    return "_".join(value.strip().lower().split())


def normalize_email(value: str) -> str:
    return value.strip().lower()


def setup_logging(log_path: Path, level: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.setLevel(getattr(logging, level.upper()))

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)


def load_rows(input_path: Path) -> list[dict[str, str]]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    logger.info("Loaded %s rows from %s", len(rows), input_path)

    return rows


def validate_lead_ref(value: str) -> str:
    normalized = value.strip().upper()

    if not LEAD_REF_RE.fullmatch(normalized):
        raise ValueError("lead_ref must match LD-0001")

    return normalized


def validate_alias(value: str, field_name: str) -> str:
    normalized = normalize_token(value)

    if not ALIAS_RE.fullmatch(normalized):
        raise ValueError(
            f"{field_name} must use lowercase letters, digits, or underscores"
        )

    return normalized


def validate_email(value: str) -> str:
    normalized = normalize_email(value)

    if not EMAIL_RE.fullmatch(normalized):
        raise ValueError("contact_email has invalid format")

    domain = normalized.rsplit("@", 1)[1]

    if domain not in ALLOWED_DEMO_DOMAINS:
        raise ValueError(
            "contact_email must use example.com or example.org in this lab"
        )

    return normalized


def validate_service(value: str) -> str:
    normalized = normalize_token(value)

    if not SERVICE_RE.fullmatch(normalized):
        raise ValueError("requested_service must be snake_case")

    return normalized


def validate_budget(value: str) -> Decimal:
    normalized = value.strip()

    try:
        amount = Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError("budget_usd must be a decimal number") from exc

    if amount <= 0:
        raise ValueError("budget_usd must be greater than 0")

    return amount.quantize(Decimal("0.01"))


def validate_due_date(value: str) -> str:
    normalized = value.strip()

    try:
        parsed = datetime.strptime(normalized, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("requested_due_date must use YYYY-MM-DD") from exc

    return parsed.isoformat()


def validate_country_code(value: str) -> str:
    normalized = value.strip().upper()

    if not COUNTRY_RE.fullmatch(normalized):
        raise ValueError("country_code must be 2 uppercase letters")

    return normalized


def derive_priority(amount: Decimal) -> str:
    return "high" if amount >= Decimal("10000.00") else "normal"


def clean_row(
    row_number: int,
    row: dict[str, str],
) -> tuple[dict[str, str] | None, dict[str, object] | None]:
    errors: list[dict[str, str]] = []

    provisional_lead_ref = raw_value(row, "lead_ref").strip().upper() or f"ROW-{row_number}"

    try:
        lead_ref = validate_lead_ref(raw_value(row, "lead_ref"))
    except ValueError as exc:
        errors.append({"field": "lead_ref", "message": str(exc)})
        lead_ref = provisional_lead_ref

    try:
        contact_alias = validate_alias(raw_value(row, "contact_alias"), "contact_alias")
    except ValueError as exc:
        errors.append({"field": "contact_alias", "message": str(exc)})
        contact_alias = ""

    try:
        validate_email(raw_value(row, "contact_email"))
    except ValueError as exc:
        errors.append({"field": "contact_email", "message": str(exc)})

    try:
        company_alias = validate_alias(raw_value(row, "company_alias"), "company_alias")
    except ValueError as exc:
        errors.append({"field": "company_alias", "message": str(exc)})
        company_alias = ""

    try:
        requested_service = validate_service(raw_value(row, "requested_service"))
    except ValueError as exc:
        errors.append({"field": "requested_service", "message": str(exc)})
        requested_service = ""

    try:
        budget = validate_budget(raw_value(row, "budget_usd"))
    except ValueError as exc:
        errors.append({"field": "budget_usd", "message": str(exc)})
        budget = Decimal("0.00")

    try:
        requested_due_date = validate_due_date(raw_value(row, "requested_due_date"))
    except ValueError as exc:
        errors.append({"field": "requested_due_date", "message": str(exc)})
        requested_due_date = ""

    try:
        country_code = validate_country_code(raw_value(row, "country_code"))
    except ValueError as exc:
        errors.append({"field": "country_code", "message": str(exc)})
        country_code = ""

    if errors:
        logger.warning(
            "Rejected row=%s lead_ref=%s error_count=%s",
            row_number,
            lead_ref,
            len(errors),
        )

        return None, {
            "row_number": row_number,
            "lead_ref": lead_ref,
            "errors": errors,
        }

    cleaned = {
        "lead_ref": lead_ref,
        "contact_alias": contact_alias,
        "company_alias": company_alias,
        "requested_service": requested_service,
        "budget_usd": f"{budget:.2f}",
        "requested_due_date": requested_due_date,
        "country_code": country_code,
        "priority": derive_priority(budget),
    }

    logger.info("Accepted row=%s lead_ref=%s", row_number, lead_ref)

    return cleaned, None


def process_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    cleaned_rows: list[dict[str, str]] = []
    error_rows: list[dict[str, object]] = []

    for row_number, row in enumerate(rows, start=2):
        cleaned, error = clean_row(row_number, row)

        if cleaned is not None:
            cleaned_rows.append(cleaned)

        if error is not None:
            error_rows.append(error)

    return cleaned_rows, error_rows


def build_summary(
    cleaned_rows: list[dict[str, str]],
    error_rows: list[dict[str, object]],
    total_rows: int,
) -> dict[str, object]:
    total_valid_budget = sum(
        (Decimal(row["budget_usd"]) for row in cleaned_rows),
        start=Decimal("0.00"),
    )

    services = Counter(row["requested_service"] for row in cleaned_rows)
    countries = Counter(row["country_code"] for row in cleaned_rows)
    priorities = Counter(row["priority"] for row in cleaned_rows)

    return {
        "total_rows": total_rows,
        "valid_rows": len(cleaned_rows),
        "invalid_rows": len(error_rows),
        "total_valid_budget_usd": f"{total_valid_budget:.2f}",
        "services": dict(services),
        "countries": dict(countries),
        "priorities": dict(priorities),
    }


def write_json(data: object, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SAFE_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and sanitize synthetic business lead data."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sample/leads_week02.csv"),
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/output/week02"),
        help="Directory for cleaned output files.",
    )

    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("logs/week02.log"),
        help="Path to the log file.",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    setup_logging(args.log_file, args.log_level)

    rows = load_rows(args.input)
    cleaned_rows, error_rows = process_rows(rows)
    summary = build_summary(cleaned_rows, error_rows, len(rows))

    write_csv(cleaned_rows, args.output_dir / "cleaned_leads.csv")
    write_json(cleaned_rows, args.output_dir / "cleaned_leads.json")
    write_json(error_rows, args.output_dir / "errors.json")
    write_json(summary, args.output_dir / "summary.json")

    logger.info("Wrote outputs to %s", args.output_dir)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()