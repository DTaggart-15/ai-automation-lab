\# Git Cheatsheet



\## Basic repository commands



Check repository status:



git status



Show current branch:



git branch --show-current



Show local branches:



git branch



Show commit history:



git log --oneline



\## Branch commands



Create and switch to a new branch:



git switch -c branch-name



Switch to an existing branch:



git switch branch-name



Delete a local branch:



git branch -d branch-name



Force delete a local branch:



git branch -D branch-name



\## Add and commit



Add all changes:



git add .



Add one file:



git add path/to/file



Create a commit:



git commit -m "commit message"



Example:



git commit -m "feat: add lead summary script"



\## Push and pull



Push a branch to GitHub:



git push -u origin branch-name



Push current branch:



git push -u origin HEAD



Pull latest changes from main:



git pull origin main



Fetch remote changes:



git fetch origin



\## Remote repository



Show remote URL:



git remote -v



Change remote URL:



git remote set-url origin https://github.com/USERNAME/REPOSITORY.git



\## Pull Request workflow



Typical workflow:



git switch main

git pull origin main

git switch -c feature-branch

git add .

git commit -m "feat: describe change"

git push -u origin feature-branch



Then on GitHub:



Pull requests -> New pull request

base: main

compare: feature-branch

Create pull request

Merge pull request



\## Useful PowerShell commands



Create a folder:



New-Item -ItemType Directory -Force -Path "folder\\name"



Create a file:



New-Item -ItemType File -Force -Path "file.txt"



Read a file:



Get-Content "file.txt"



Check if a file exists:



Test-Path "file.txt"



Write text to a file:



Set-Content -Encoding UTF8 "file.txt" "content here"



\## Python project commands



Install project in editable mode:



python -m pip install -e .



Run smoke-script:



python -m ai\_automation\_lab.main --input data/sample/leads.csv --output data/output/summary.json



Run unit tests:



python -m unittest discover



Run unit tests with detailed output:



python -m unittest discover -v



\## Common mistakes and fixes



\### Mistake: running a folder path as a command



Wrong:



C:\\Users\\gost\\ai-automation-lab\\ai-automation-lab>



Correct:



cd C:\\Users\\gost\\ai-automation-lab\\ai-automation-lab



\### Mistake: using Linux touch in PowerShell



Wrong:



touch file.txt



Correct:



New-Item -ItemType File -Force -Path "file.txt"



\### Mistake: Python cannot find the module



Error:



ModuleNotFoundError: No module named 'ai\_automation\_lab'



Fix:



python -m pip install -e .



Temporary fix:



$env:PYTHONPATH="$PWD\\src"



\### Mistake: committing generated files



Do not commit:



.venv/

\_\_pycache\_\_/

\*.pyc

.pytest\_cache/

.env

\*.egg-info/

data/output/\*.json



\## Commands practiced this week



Git commands:



\- git status

\- git branch

\- git branch --show-current

\- git switch

\- git switch -c

\- git add

\- git commit

\- git push

\- git pull

\- git fetch

\- git remote -v

\- git remote set-url

\- git log --oneline

\- git branch -d



Python commands:



\- python -m pip install -e .

\- python -m ai\_automation\_lab.main --input data/sample/leads.csv --output data/output/summary.json

\- python -m unittest discover

\- python -m unittest discover -v



PowerShell commands:



\- cd

\- dir

\- pwd

\- Test-Path

\- Get-Content

\- Set-Content

\- New-Item

\- Remove-Item



\## Week 01 result



I practiced the full GitHub workflow:



\- created a public repository;

\- created project branches;

\- committed changes;

\- pushed branches to GitHub;

\- opened Pull Requests;

\- merged Pull Requests into main;

\- fixed branch and remote issues;

\- cleaned generated files from Git;

\- ran a Python smoke-script;

\- ran unit tests successfully.



Final result: the repository is ready for future AI automation practice tasks.

