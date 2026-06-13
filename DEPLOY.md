# Deploying to PythonAnywhere

Canonical live path on PythonAnywhere:

```text
/home/zeshi2personal/personal-website
```

This repository should be updated locally first, committed, pushed to GitHub `main`, and only then pulled on PythonAnywhere. Do not deploy or mutate the PythonAnywhere live state without explicit approval.

## Local pre-deploy checklist

From `/home/zeshi/Desktop/codex/personal-website`:

```bash
git status --short
python3 -m py_compile app.py database.py manage_content.py
python3 -m flask --app app routes
```

Confirm before commit/push:

- `git status --short` contains only intentional source/doc edits.
- No runtime files are tracked: `test.db`, `*.db`, `*.sqlite3`, `.DS_Store`, `__pycache__/`, or `*.pyc`.
- Public route smoke checks pass locally if the change affects templates/routes.

## PythonAnywhere handoff commands

After local changes are committed and pushed to GitHub, SSH or open a PythonAnywhere Bash console and run:

```bash
cd /home/zeshi2personal/personal-website
git status --short
git pull origin main
python3 -m py_compile app.py database.py manage_content.py
```

Then reload the web app from the PythonAnywhere dashboard:

1. Open the **Web** tab.
2. Select the Zeshi personal website web app.
3. Click **Reload**.
4. Visit the public site and spot-check the changed pages.

If `git status --short` on PythonAnywhere shows unexpected local modifications before pulling, stop and preserve/report them instead of overwriting live state.
