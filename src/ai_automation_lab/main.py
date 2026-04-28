from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def load_leads(input_path: Path) -> list[dict[str, str]]:
    """
    Reads leads from a CSV file and returns a list of dictionaries.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        leads = list(reader)

    logger.info("Loaded %s leads from %s", len(leads), input_path)
    return leads


def build_summary(leads: list[dict[str, str]]) -> dict[str, int]:
    """
    Builds a simple summary from lead data.
    """
    total_budget = 0

    for lead in leads:
        raw_budget = lead.get("budget_usd", "0")

        try:
            total_budget += int(raw_budget)
        except ValueError:
            logger.warning("Invalid budget value: %s", raw_budget)

    return {
        "total_leads": len(leads),
        "total_budget_usd": total_budget,
    }


def save_json(data: dict[str, int], output_path: Path) -> None:
    """
    Saves dictionary data to a JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info("Saved summary to %s", output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a simple summary from a leads CSV file."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/sample/leads.csv"),
        help="Path to input CSV file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/summary.json"),
        help="Path to output JSON file.",
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

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    leads = load_leads(args.input)
    summary = build_summary(leads)
    save_json(summary, args.output)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
