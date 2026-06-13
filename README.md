# Personal Website

Flask personal portfolio site for Zeshi Yang, with editable content stored in a local SQLite database.

## Repository layout

- `app.py` — Flask app, routes, content-admin views, and database schema migration helpers.
- `database.py` / `schema.sql` — local database initialization helpers.
- `templates/` — Jinja templates for public and admin pages.
- `static/` — images, CSS, and other public assets.
- `requirements.txt` — pinned Python dependencies used by the app.
- `DEPLOY.md` — PythonAnywhere deployment and reload workflow.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export SITE_ADMIN_PASSWORD='local-preview-only'
flask run --host=127.0.0.1 --port=3055
```

A convenience script is also available:

```bash
PORT=3055 ./run-local.sh
```

The app creates/updates `test.db` at runtime. Keep local runtime artifacts out of Git: `test.db`, `*.db`, `*.sqlite3`, `.venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`, and local environment files are intentionally ignored.

## Verification before handoff

Run the smallest checks before committing or handing deployment to PythonAnywhere:

```bash
python3 -m py_compile app.py database.py manage_content.py
python3 -m flask --app app routes
```

For a route smoke test, start the app locally and check `/`, `/academic_research/`, `/investment_research/`, `/contact`, and `/admin/login`. The legacy `/trading` route currently returns 404 by design.

## Deployment

This repo is mirrored to GitHub `main` and is deployed on PythonAnywhere from:

```text
/home/zeshi2personal/personal-website
```

Do not edit PythonAnywhere live files directly unless explicitly approved. Make and verify changes locally, commit/push to GitHub, then follow `DEPLOY.md` for the PythonAnywhere `git pull` + Web tab reload handoff.
