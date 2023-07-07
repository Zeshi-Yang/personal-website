DROP TABLE IF EXISTS introductions;
CREATE TABLE introductions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
    full_title TEXT NOT NULL,
);
INSERT INTO introductions (title, content) VALUES ('Binder Jetting', 'Introduction to Binder Jetting...');
INSERT INTO introductions (title, content) VALUES ('Laser Powder Bed Fusion', 'Introduction to Laser Powder Bed Fusion...');