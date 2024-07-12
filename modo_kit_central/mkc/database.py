from typing import List
import sqlite3

from .prefs import Paths, AuthorData


def search_kits(search_text: str) -> List[int]:
    """Searches the database for the given search text.

    Args:
        search_text: The text to search for.
    """
    # Split the search text into individual terms.
    search_terms = [s.strip() for s in search_text.split(",")]

    # Generate the search query for all terms.
    query = "SELECT * FROM kits WHERE 1=1"
    params = []

    for term in search_terms:
        query += " AND (name LIKE ? OR author LIKE ? OR search LIKE ? OR Description LIKE ?)"
        params.extend([f"%{term}%"] * 4)

    with sqlite3.connect(Paths.DATABASE) as connection:
        cursor = connection.cursor()
        # Search all fields in kits table for the search text.
        cursor.execute(query, params)
        # Get id of all matching kits and remap from 1-indexed to 0-indexed.
        return [kit[0] - 1 for kit in cursor.fetchall()]


def get_kits() -> List[tuple]:
    """Gets all kits from the database.

    Returns:
        kits: A list of all kits in the database.
    """
    with sqlite3.connect(Paths.DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kits")
        return cursor.fetchall()


def get_author(author: str) -> AuthorData:
    """Gets the author data from the database.

    Args:
        author: The author's name to get data for.

    Returns:
        author_data: The author's data class.
    """
    with sqlite3.connect(Paths.DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE name=?",
            (author,)
        )
        return AuthorData(*cursor.fetchone())
