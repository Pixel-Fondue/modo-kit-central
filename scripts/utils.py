from typing import List
from pathlib import Path

import toml


class Paths:
    """Class to store the paths used in the project."""
    REPO_ROOT = Path(__file__).parent.parent.absolute()


def make_index(folder: Path, files: List[Path], message: str, restart="No") -> str:
    """Method to generate the body of an index.xml for packaging example files.

    Args:
        folder: The name of the folder.
        files: List of files in the folder.
        message: The message to display to the user after installing the lpk.
        restart: If the lpk should present the restart message to the user.

    Returns:
        xml: the generated index.xml template as a string.
    """
    # Header
    xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    # Modo 10+
    xml += "\n<package version=\"1000\">"
    # No need to restart
    restart = "YES" if restart else "NO"
    xml += f'\n\t<kit name="{folder.name}" restart="{restart}">'
    # For each file add target
    for file in files:
        # Path including the kit directory
        full_path = file.relative_to(folder.parent)
        # Path without kit directory. Modo requires that paths in the index use forward slash
        rel_path = file.relative_to(folder)
        xml += f'\n\t\t<source target="{full_path.as_posix()}">{rel_path.as_posix()}</source>'
    # Add license file
    xml += f'\n\t\t<source target="{folder.name}\\LICENSE">LICENSE</source>'
    # Add user facing message
    xml += f'\n\t</kit>\n\t<message button="Help">{message}</message>\n</package>'
    # Return Text
    return xml


def get_pyproject() -> dict:
    """Gets the data from the pyproject file.

    Returns:
        project_data: The data from the pyproject.toml file.
    """
    pyproject = Paths.REPO_ROOT / "pyproject.toml"

    with pyproject.open('r') as project_file:
        project_data = toml.load(project_file)

    return project_data


def get_version(project: dict) -> str:
    """Gets the version number from the pyproject file.

    Args:
        project: The data from the pyproject file.

    Returns:
        The version number from the pyproject file.
    """
    return project.get('project', {}).get('version', "0.0.0")


def readable_size(size: int, decimal: int = 2) -> str:
    """Converts a byte size into a human-readable format.

    Args:
        size: The size in bytes.
        decimal: The number of decimal places to display.

    Returns:
        The size in a human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0:
            return f"{size:.{decimal}f} {unit}"
        size /= 1024.0

    return f"{size:.{decimal}f} {unit}"
