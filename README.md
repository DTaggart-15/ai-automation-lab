\# ai-automation-lab



Public learning repository for practicing Python, GitHub workflow, unit tests, and small AI automation projects.



The repository is used as a sandbox for practical tasks: project skeletons, smoke-scripts, automation experiments, documentation, and reproducible workflows.



\## Project goals



The main goals of this repository are:



\- practice Git and GitHub workflow;

\- create clean project structures;

\- work with branches and Pull Requests;

\- write small Python automation scripts;

\- use synthetic sample data;

\- run unit tests;

\- document learning progress.



\## Project structure



```text

ai-automation-lab/

├── data/

│   ├── sample/

│   │   └── leads.csv

│   └── output/

│       └── .gitkeep

├── docs/

│   └── week-01.md

├── notes/

│   └── git-cheatsheet.md

├── src/

│   └── ai\_automation\_lab/

│       ├── \_\_init\_\_.py

│       └── main.py

├── tests/

│   ├── \_\_init\_\_.py

│   └── test\_main.py

├── .env.example

├── .gitignore

├── README.md

└── pyproject.toml

Week 01 task

Week 01 focused on:

creating a public GitHub repository;
creating the initial project skeleton;
adding a Python smoke-script;
adding unit tests;
documenting Git commands and weekly results;
merging changes into main through Pull Requests.
Smoke-script

The script reads synthetic lead data from:

data/sample/leads.csv

It calculates:

total number of leads;
total budget in USD;
saves the result to JSON;
prints the result in the terminal.

Run:

python -m ai_automation_lab.main --input data/sample/leads.csv --output data/output/summary.json

Expected output:

{
  "total_leads": 4,
  "total_budget_usd": 32000
}
Unit tests

Run:

python -m unittest discover

Expected result:

OK
Installation for local development

Install the project in editable mode:

python -m pip install -e .
Data policy

Only synthetic sample data is used in this repository.

Do not commit:

real client data;
real emails;
invoices;
private documents;
private messages;
API keys;
.env files;
generated output files.
Useful files
docs/week-01.md — Week 01 learning summary.
notes/git-cheatsheet.md — Git and PowerShell command notes.
src/ai_automation_lab/main.py — Python smoke-script.
tests/test_main.py — unit tests.
data/sample/leads.csv — synthetic sample lead data.
Current status

Week 01 is completed:

repository created;
project skeleton created;
smoke-script works;
unit tests pass;
notes are filled;
changes were merged into main through Pull Requests.

