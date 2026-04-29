# Week 01 — GitHub Workflow and Project Skeleton

## Goal

The goal of Week 01 was to create a clean public GitHub repository and practice the basic development workflow for future AI automation projects.

Main goals:

- create a public GitHub repository;
- create and use branches;
- make commits;
- open Pull Requests;
- merge changes into main;
- create a basic Python project skeleton;
- run a Python smoke-script;
- add and run unit tests;
- document the commands and results.

## What I practiced

During this week I practiced:

- creating a GitHub repository;
- creating branches;
- switching between branches;
- checking repository status;
- adding files to Git;
- making commits;
- pushing branches to GitHub;
- creating Pull Requests;
- merging Pull Requests into main;
- fixing an incorrect remote URL;
- cleaning unnecessary files from Git;
- using .gitignore;
- creating a Python package structure;
- running a Python module with python -m;
- installing the project in editable mode;
- writing and running unit tests.

## Final project structure

The project contains:

- src/
- tests/
- data/sample/
- data/output/
- docs/
- notes/
- README.md
- pyproject.toml
- .gitignore
- .env.example

## Smoke-script

The smoke-script reads lead data from:

data/sample/leads.csv

It calculates:

- total number of leads;
- total budget in USD;
- saves the result to JSON;
- prints the JSON result in the terminal.

Command:

python -m ai_automation_lab.main --input data/sample/leads.csv --output data/output/summary.json

Expected result:

{
  "total_leads": 4,
  "total_budget_usd": 32000
}

## Unit tests

Command:

python -m unittest discover

Expected result:

OK

The tests check:

- loading leads from CSV;
- calculating summary values;
- saving summary data to JSON.

## Questions and short answers

### Why do we use branches?

Branches allow us to work on changes separately from main. This makes the workflow safer because unfinished work does not immediately affect the stable version of the project.

### Why do we use Pull Requests?

Pull Requests show the difference between a feature branch and main. They make it easier to review changes, track history, and merge work in a controlled way.

### Why should changes go into main through Pull Requests?

This keeps the project history clean. It also creates a visible record of what was changed, when it was changed, and why it was changed.

### Why do we use .gitignore?

.gitignore prevents unnecessary files from being committed. Examples: virtual environments, cache files, .pyc files, local .env files, and generated output files.

### Why do we use .gitkeep?

Git does not track empty folders. .gitkeep allows us to keep an otherwise empty folder, such as data/output/, in the repository.

### Why do we use unit tests?

Unit tests help verify that the code works correctly after changes. They reduce the risk of breaking existing functionality.

### Why did we use synthetic data?

Synthetic data is safe for public repositories. Real client names, emails, invoices, documents, and private messages should not be committed.

## Result of the week

By the end of Week 01:

- the public repository ai-automation-lab was created;
- the project skeleton was created;
- the Python smoke-script was implemented;
- the script successfully reads CSV data and writes JSON output;
- unit tests were added and passed;
- changes were merged into main through Pull Requests;
- GitHub workflow was practiced from branch creation to PR merge.

Week 01 result: basic GitHub and Python project workflow is ready for future AI automation tasks.
