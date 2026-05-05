\# Week 02 — Safe Data Cleaner



\## Goal



The goal of Week 02 was to build a safe CSV data cleaner for basic automation workflows.



The tool reads a dirty CSV file, cleans column names and text values, removes fully empty rows, masks sensitive fields, and saves a cleaned CSV file together with a JSON report.



\## What I practiced



During this week I practiced:



\- creating a new Python module;

\- writing tests before final implementation;

\- cleaning CSV data;

\- normalizing column names;

\- cleaning text values;

\- removing empty rows;

\- masking sensitive data;

\- saving cleaned CSV files;

\- saving JSON reports;

\- running a Python module from PowerShell;

\- checking project status with Git.



\## Files created



Main module:



```text

src/ai\_automation\_lab/week02\_safe\_cleaner.py

Tests:



tests/test\_week02\_safe\_cleaner.py



Sample input:



data/sample/week02\_dirty\_leads.csv



Generated output:



data/output/week02/clean\_leads.csv

data/output/week02/clean\_report.json

What the cleaner does



The cleaner performs the following operations:



Normalizes column names.



Example:



Full Name -> full\_name

Email Address -> email\_address

Phone-Number -> phone\_number

Budget USD -> budget\_usd

Cleans text values.



Example:



"  Anna   Petrova  " -> "Anna Petrova"

Removes fully empty rows.



Rows where all values are empty are not written to the cleaned output file.



Masks email addresses.



Example:



anna@example.com -> a\*\*\*@example.com

x@test.com -> \*\*\*@test.com

Masks phone numbers.



Example:



+7 999 123-45-67 -> +7\*\*\*\*\*\*\*\*67

89991234567 -> 8\*\*\*\*\*\*\*\*67

Saves a JSON report.

