-- Desc: Insert a new kit into the database
INSERT INTO kits (
    name, author, version, description, url, help, installable, search
) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
