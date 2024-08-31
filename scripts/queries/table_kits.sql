-- Create the kits table
CREATE TABLE IF NOT EXISTS kits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    label TEXT,
    author TEXT,
    version TEXT,
    description TEXT,
    url TEXT,
    help TEXT,
    installable BOOLEAN,
    search TEXT
);
