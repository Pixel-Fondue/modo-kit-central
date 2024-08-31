-- Desc: Insert a new kit into the database
INSERT INTO kits (
    name, label, author, version, description, url, help, installable, search
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
