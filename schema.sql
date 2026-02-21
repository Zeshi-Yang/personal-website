CREATE TABLE IF NOT EXISTS research_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    full_title TEXT NOT NULL,
    display_order INTEGER
);

CREATE TABLE IF NOT EXISTS programming_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    full_title TEXT NOT NULL,
    display_order INTEGER
);

CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    question TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS site_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    headline TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    location TEXT NOT NULL,
    introduction TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS project_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    caption TEXT DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_project_images_section_project
ON project_images(section, project_id, sort_order, id);
