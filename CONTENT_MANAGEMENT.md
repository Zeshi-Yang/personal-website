# Content Management Guide

This site now supports profile, project text, ordering, and image management.

## Browser Admin (recommended)

1. Set an admin password:
   ```bash
   export SITE_ADMIN_PASSWORD='choose-a-strong-password'
   ```
2. Start the app:
   ```bash
   flask --app app run --debug
   ```
3. Login:
   - `http://127.0.0.1:5000/admin/login`

## What you can do in admin

- Edit profile content:
  - `http://127.0.0.1:5000/admin/profile`
- Manage investment entries:
  - `http://127.0.0.1:5000/admin/projects/investment`
- Manage academic entries:
  - `http://127.0.0.1:5000/admin/projects/academic`

Per project section you can:
- Add new entries
- Edit title/full title/content
- Reorder entries with Up/Down
- Delete entries
- Add images (upload file or existing static path)
- Reorder images with Up/Down
- Delete images

## Image management strategy

- New uploads are stored under:
  - `static/images/uploads/investment/`
  - `static/images/uploads/academic/`
- Existing legacy images under `static/images/programming/` and `static/images/research/` are auto-seeded into DB on startup.
- Image references are tracked in `project_images` table (no more implicit file-name-by-id rules).

## CLI helper (optional)

### Show profile
```bash
python manage_content.py profile show
```

### Update profile fields
```bash
python manage_content.py profile update \
  --name "YANG Zeshi, Ph.D." \
  --headline "VC Analyst | Investment Research"
```

### List projects
```bash
python manage_content.py project list --section investment
python manage_content.py project list --section academic
```

## Notes

- Database file: `test.db`
- Hidden page: `/trading` currently returns 404.
- Before public deployment, replace simple session-password admin with production-grade auth.
