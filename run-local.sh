#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
export FLASK_APP=app.py
export SITE_ADMIN_PASSWORD=${SITE_ADMIN_PASSWORD:-local-preview-only}
export CONTACT_NOTIFY_TO=${CONTACT_NOTIFY_TO:-}
flask run --host=0.0.0.0 --port=${PORT:-3055}
