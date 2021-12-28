import os
from os import mkdir
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED

import utils
from utils import mid_header
from utils import mid_root
from utils import mid_configs
from utils import mid_lxserv
from utils import mid_message
from utils import mid_resources

# Get the root path to this repo
repo_dir = Path(__file__).parent

kit_name = "community_hub"
# Get the kit directories
kit_dir = repo_dir / "community_hub"
configs_dir = kit_dir / "configs"
lxserv_dir = kit_dir / "lxserv"
resources_dir = kit_dir / "resources"
# Get the build directory
build_dir = repo_dir / "build"
# Get the license file
license_file = repo_dir / "LICENSE"


# Get all files in the kit directory and make sure no pyc files come along.
def root_fi():
    # Get Base files for a kit description index.cfg
    root_files = []
    files = [f for f in os.listdir(kit_dir) if f.endswith(".cfg") or f.endswith(".txt")]
    for f in files:
        f = kit_dir / f
        root_files.append(f)
    # licen = [f for f in os.listdir(kit_dir) if f.endswith("cense")]
    # for f in licen:
    #     f = kit_dir / f
    #     root_files.append(f)
    print("INDEX ----- Root files -----")
    print(root_files)
    return root_files
# root_fi()

# Files contained in the "config" folder
def configs_fi():
    # Get Base files in folders "configs" and make sure no pyc files come along
    configs_files = [f for f in configs_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print("INDEX ----- files in configs folder -----")
    print(configs_files)
    return configs_files
# config_fi()

# Files contained in the "lxserv" folder and make sure no pyc files come along
def lxserv_fi():
    lxserv_files = [f for f in lxserv_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print("INDEX ----- files in lxserv folder -----")
    print(lxserv_files)
    return lxserv_files
# lxserv_fi()

# Files contained in the "scripts" folder
def resources_fi():
    # Get Base files in folders "resources" and make sure no pyc files come along
    resources_files = [f for f in resources_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print("INDEX ----- files in resources folder -----")
    print(resources_files)
    return resources_files
# resources_fi()



# Clear the build directory
if build_dir.exists():
    rmtree(build_dir)
# Remake the build directory
mkdir(build_dir)

# Format the lpk file name with the version number from the VERSION file
version = utils.get_version()
lpk_path = build_dir / f"community_hub_{version}.lpk"
# Message to display to the users
message = f"Successfully installed Modo Community Hub: v{version}"

# Build the LPK file.
with ZipFile(lpk_path, mode="w", compression=ZIP_DEFLATED) as lpk:
    # Add the license
    # lpk.write(license_file, "license")

    # Generate the index.xml file data
    indexheader = mid_header(name=kit_name, restart="YES")

    ###### ModoComHub BASE STRUCTURE
    print("----- Copy Root Data -----")
    indexroot = mid_root(folder=kit_dir, files=root_fi())

    print("----- Copy Root/configs Folder Data -----")
    indexconfigs = mid_configs(folder=kit_dir, files=configs_fi())

    print("----- Copy Root/lxserv Folder Data -----")
    indexlxserv = mid_lxserv(folder=kit_dir, files=lxserv_fi())

    print("----- Copy Root/resources Folder Data -----")
    indexresources = mid_resources(folder=kit_dir, files=resources_fi())

    ###### MESSAGE
    indexmessage = mid_message(info=message)

    # Write the index.xml file
    index_data = (indexheader + indexroot + indexconfigs + indexmessage)
    # index_data = (indexheader + indexroot + indexconfigs + indexlxserv + indexresources + indexmessage)
    lpk.writestr("index.xml", index_data)

    # Write all file into the lpk
    print("----- Root files -----")
    for file in root_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- configs folder files -----")
    for file in configs_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- lxserv Folder files -----")
    for file in lxserv_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- resources Folder files -----")
    for file in resources_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))


