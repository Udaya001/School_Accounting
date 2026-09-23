# Backend

Requires Python 3.12+ and PostgreSQL for database-backed work. From this directory, create a virtual environment, install the project with `pip install -e '.[dev]'`, copy `.env.example` to `.env`, then run `uvicorn school_accounting.main:app --reload --app-dir src`. Run checks with `pytest` and Alembic with `alembic upgrade head`.

The health endpoint is `GET /health`. The initial scaffold contains no domain tables or migrations.
