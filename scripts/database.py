# Creates a database for loading kit info
import json
from sqlite3 import Cursor, connect

from scripts.prefs import Paths
from scripts.utils import readable_size


def load_queries() -> dict[str, str]:
    """Loads all query files from SCRIPT_QUERIES.

    Returns:
        queries: A dictionary of query names and their contents.
    """
    queries = {}
    for query in Paths.SCRIPT_QUERIES.glob("*.sql"):
        with query.open('r') as file:
            queries[query.stem] = file.read()

    return queries


def populate_kits(cursor: Cursor) -> None:
    """Populates the kits table with data from `kits.json`.

    Notes:
        name, author, version, description, url, help, installable, search

    Args:
         cursor: The database cursor.
    """
    kits_data = json.loads(Paths.KIT_DATA.read_text())

    for kit_name, kit_info in kits_data.items():
        cursor.execute(
            QUERY_DATA['insert_kit'],
            (
                kit_name,
                kit_info.get('author'),
                kit_info.get('version'),
                kit_info.get('description'),
                kit_info.get('url'),
                kit_info.get('help'),
                kit_info.get('installable', False),
                ",".join(kit_info.get("search"))
            )
        )


def populate_authors(cursor: Cursor) -> None:
    """Populates the authors table with data from `authors.json`.

    Args:
        cursor: The database cursor.
    """
    authors_data = json.loads(Paths.AUTHOR_DATA.read_text())

    for author_name, author_info in authors_data.items():
        cursor.execute(
            QUERY_DATA['insert_author'],
            (
                author_name,
                author_info.get('avatar'),
                author_info.get('handle'),
                json.dumps(author_info.get('links'))
            )
        )


def build_database() -> None:
    """Builds the database for all kits in `kits.json`."""
    # Delete the database if it exists.
    if Paths.KIT_DATABASE.exists():
        Paths.KIT_DATABASE.unlink()

    # Create database with the kits' data.
    with connect(Paths.KIT_DATABASE) as connection:
        # Initialize the database.
        cursor = connection.cursor()
        cursor.execute("PRAGMA page_size = 1024")
        cursor.execute("VACUUM")
        # Create the table for the kits.
        cursor.execute(QUERY_DATA['table_kits'])
        # Create the table for the authors.
        cursor.execute(QUERY_DATA['table_authors'])
        # Populate the kits table.
        populate_kits(cursor)
        # Populate the authors table.
        populate_authors(cursor)

    # Print the size of the files to ensure nothing goofy is happening.
    print(".json:", readable_size(Paths.KIT_DATA.stat().st_size + Paths.AUTHOR_DATA.stat().st_size))
    print(".db:", readable_size(Paths.KIT_DATABASE.stat().st_size))


if __name__ == '__main__':
    """Builds the database for all kits in `kits.json`."""
    QUERY_DATA = load_queries()
    build_database()
