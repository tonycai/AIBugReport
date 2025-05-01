# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Build: `pip install -r requirements.txt` or `pip install -e .`
- Run: `aibug <command>` (report, list, view)
- Test: `pytest tests/` or `pytest tests/test_specific.py -v`
- Test single: `pytest tests/test_file.py::test_function -v`
- Frontend: `cd frontend && npm install && npm run dev`
- Docker: `docker-compose up --build`

## Code Style Guidelines
- Follow PEP 8 conventions for Python code
- Use docstrings for modules, classes, functions
- Imports: standard library first, then third-party, then local
- Type hints: Use for function parameters and return values
- Error handling: Use try/except with specific exceptions
- Variable naming: snake_case for variables/functions, PascalCase for classes
- Frontend: JavaScript/Node.js standard conventions with ES6 syntax
- Environment variables for configuration (DB, API keys, etc.)