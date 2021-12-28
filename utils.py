from pathlib import Path

# Get the root path to this repo
repo_dir = Path(__file__).parent

""" Method to generate the body of an index.xml for packaging example files.

Args:
    folder (Path): The name of the folder.
    files (list(Path)): List of files in the folder.
    message (str): The message to display to the user after installing the lpk.
    restart (bool): If the lpk should present the restart message to the user.

Returns:
    xml (str): the generated index.xml template.
"""

###### Create the XML file header for the index.xml file  (packed in the lpk to unzip files to corresponding directory)
###### mid stands for "MakeIndex"
def mid_header(name, restart="No"):
    # Header
    xml_header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    # Modo 10+
    xml_header += "\n<package version=\"1000\">"
    # No need to restart
    restart = "YES" if restart else "NO"
    xml_header += f'\n\t<kit name="{name}" restart="{restart}">'
    return xml_header

def mid_root(folder, files):
    # For each file add target
    xml_root = f''
    for file in files:  # type: Path
        # Path including the kit directory
        root_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        root_rel_path = file.relative_to(folder)
        xml_root += f'\n\t\t<source target="{root_full_path}">{root_rel_path}</source>'
    # print (xml_root)
    # Return Text
    return xml_root

def mid_configs(folder, files):
    # For each file add target
    xml_configs = f''
    for file in files:  # type: Path
        # Path including the kit directory
        configs_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        configs_rel_path = file.relative_to(folder)
        xml_configs += f'\n\t\t<source target="{configs_full_path}">{configs_rel_path}</source>'
    # print (xml_configs)
    return xml_configs

def mid_resources(folder, files):
    # For each file add target
    xml_resources = f''
    for file in files:  # type: Path
        # Path including the kit directory
        resources_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        resources_rel_path = file.relative_to(folder)
        xml_resources += f'\n\t\t<source target="{resources_full_path}">{resources_rel_path}</source>'
    # print (xml_resources)
    return xml_resources

def mid_lxserv(folder, files):
    # For each file add target
    xml_lxserv = f''
    for file in files:  # type: Path
        # Path including the kit directory
        lxserv_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        lxserv_rel_path = file.relative_to(folder)
        xml_lxserv += f'\n\t\t<source target="{lxserv_full_path}">{lxserv_rel_path}</source>'
    return xml_lxserv

def mid_message(info):
    xml_message = f'\n\t</kit>\n\t<message button="Help">{info}</message>\n</package>'
    return xml_message


def get_version():
    with repo_dir.joinpath("VERSION").open("r") as version_file:
        return version_file.read().strip()
