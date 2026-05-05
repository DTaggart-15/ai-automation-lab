# Week 02 — Safe Local Data Cleaner

## Goal

Build a local Python CLI that reads synthetic CSV data, validates rows, writes safe CSV/JSON outputs, and avoids storing direct contact data in outputs and logs.

## What I practiced

- pathlib
- csv.DictReader / DictWriter
- json output
- argparse CLI
- logging
- regex validation
- Decimal for money
- unittest
- PowerShell file operations

## Safety rules

- synthetic data only
- example domains only
- no real customer data
- no secrets in repo
- no raw row dumps in logs
- cleaned outputs exclude contact_email

## Produced files

- data/output/week02/cleaned_leads.csv
- data/output/week02/cleaned_leads.json
- data/output/week02/errors.json
- data/output/week02/summary.json
- logs/week02.log

## Input file

- data/sample/leads_week02.csv

## Main module

- src/ai_automation_lab/week02_safe_cleaner.py

## Tests

- tests/test_week02_safe_cleaner.py

## CLI command

```powershell
.\.venv\Scripts\python.exe -m ai_automation_lab.week02_safe_cleaner --input .\data\sample\leads_week02.csv --output-dir .\data\output\week02 --log-file .\logs\week02.log
```

## Expected summary

```json
{
  "total_rows": 6,
  "valid_rows": 3,
  "invalid_rows": 3,
  "total_valid_budget_usd": "25200.50",
  "services": {
    "invoice_automation": 1,
    "support_triage": 1,
    "document_extraction": 1
  },
  "countries": {
    "GB": 1,
    "DE": 1,
    "NL": 1
  },
  "priorities": {
    "normal": 2,
    "high": 1
  }
}
```

## Questions to review

1. Why use Decimal instead of float for money?
2. Why open CSV files with newline=''?
3. Why use pathlib instead of hardcoded path strings?
4. Why validate email but exclude it from safe output?
5. What should never be written to logs?
6. What does argparse give us?
7. What do unit tests protect against?

## Result

Week 02 now contains a safe local data cleaner with validation, sanitized outputs, structured JSON reports, and logging.