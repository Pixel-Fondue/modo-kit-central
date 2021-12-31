from pathlib import Path

# Get the root path to this repo
repo_dir = Path(__file__).parent


def make_index(folder, files, message, restart="No"):
    """ Method to generate the body of an index.xml for packaging example files.

    Args:
        folder (Path): The name of the folder.
        files (list(Path)): List of files in the folder.
        message (str): The message to display to the user after installing the lpk.
        restart (bool): If the lpk should present the restart message to the user.

    Returns:
        xml (str): the generated index.xml template.
    """
    # Header
    xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    # Modo 10+
    xml += "\n<package version=\"1000\">"
    # No need to restart
    restart = "YES" if restart else "NO"
    xml += f'\n\t<kit name="{folder}" restart="{restart}">'
    # For each file add target
    for file in files:  # type: Path
        # Path including the kit directory
        full_path = file.relative_to(folder.parent)
        # Path without kit directory. Modo requires that paths in the index use forward slash
        rel_path = fwd_slash(file.relative_to(folder))
        xml += f'\n\t\t<source target="{full_path}">{rel_path}</source>'
    # Add license file
    xml += f'\n\t\t<source target="community_hub\LICENSE">LICENSE</source>'
    # Add user facing message
    xml += f'\n\t</kit>\n\t<message button="Help">{message}</message>\n</package>'
    # Return Text
    return xml


def fwd_slash(file_path):
    """Ensure that all slashes are /

    Args:
        file_path (str): The path to force /

    Returns:
        (str): Formatted path
    """
    return str(file_path).replace("\\", "/")


def get_version():
    """Gets the version number from the VERSION file.

    Returns:
        (str): The version number from the VERSION file.
    """
    with repo_dir.joinpath("VERSION").open("r") as version_file:
        return version_file.read().strip()
