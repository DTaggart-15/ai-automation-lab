# ai-automation-lab

Starter repository for experiments, notes, and small automation workflows in Python.

## Layout

- `src/ai_automation_lab/`: application package
- `tests/`: automated tests
- `data/sample/`: sample input data
- `data/output/`: generated output data
- `docs/`: weekly notes and project docs
- `notes/`: quick references and cheatsheets

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
python -m ai_automation_lab.main
```
# AI Automation Lab

Учебный репозиторий для освоения AI automation for business.

## Цель

Научиться проектировать и разрабатывать бизнес-автоматизации на Python, FastAPI, PostgreSQL, Docker, LLM API, tool calling, embeddings, RAG, vector DB, LangChain/LangGraph и n8n.

## Текущий статус

Неделя 1: GitHub workflow, структура проекта, первый Python smoke-script.

## Стек, который будет использоваться

- Python
- Git / GitHub
- PostgreSQL
- FastAPI
- Docker / Docker Compose
- LLM API
- Structured outputs
- Tool/function calling
- Embeddings
- RAG
- Qdrant / pgvector
- LangChain / LangGraph
- n8n

## Структура проекта

```text
ai-automation-lab/
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── src/
│   └── ai_automation_lab/
├── tests/
├── data/
│   ├── sample/
│   └── output/
├── docs/
└── notes/
