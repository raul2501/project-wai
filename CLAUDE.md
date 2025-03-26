# Wai Project Guidelines

## Build & Run Commands
- Backend: `python backend/server.py`
- Scripts: `python scripts/notion_test.py`
- Frontend: TBD (likely JavaScript/web-based)

## Testing
- Run tests: `pytest tests/`
- Single test: `pytest tests/path_to_test.py::test_function_name -v`

## Code Style Guidelines
- **Python**: Follow PEP 8 standards
- **Imports**: Group standard lib, third-party, and local imports
- **Naming**: snake_case for variables/functions, CamelCase for classes
- **Type Hints**: Use Python type annotations where possible
- **Error Handling**: Use try/except blocks with specific exceptions
- **Documentation**: Docstrings for functions and classes
- **Line Length**: Limit to 88 characters
- **Formatting**: Use Black for Python code formatting

## Linting
- Python: `flake8 . --exclude=venv/`
- Code format: `black .`