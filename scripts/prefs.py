"""All paths related to building the project."""
from dataclasses import dataclass
from pathlib import Path

import toml


@dataclass
class Project:
    """Project data from pyproject.toml."""
    DATA = toml.load("pyproject.toml")
    POETRY = DATA['tool']['poetry']
    NAME = POETRY['name']
    VERSION = POETRY['version']
    DESCRIPTION = POETRY['description']
    KIT = DATA['modo']['kit']
    KIT_LABEL = KIT['label']
    LPK_NAME = KIT['lpk_name']


@dataclass(frozen=True)
class Paths:
    """All paths related to building the project."""
    REPO_ROOT = Path(__file__).parent.parent.absolute()
    # Kit paths
    KIT = REPO_ROOT / Project.NAME
    KIT_RESOURCES = KIT / "resources"
    KIT_DATABASE = KIT_RESOURCES / "kits.db"
    KIT_VERSION = KIT / "mkc" / "version.py"
    KIT_INDEX = KIT / "index.cfg"
    # Tooling paths
    SCRIPTS = REPO_ROOT / "scripts"
    SCRIPTS_RESOURCES = SCRIPTS / "resources"
    # Data paths
    KIT_DATA = SCRIPTS_RESOURCES / "kits.json"
    AUTHOR_DATA = SCRIPTS_RESOURCES / "authors.json"
    # Build paths
    BUILD = REPO_ROOT / "build"
    LICENSE = REPO_ROOT / "LICENSE"
    ZIP_INDEX = "index.xml"
    ZIP_LICENSE = "LICENSE"
    LPK_OUTPUT = BUILD / Project.LPK_NAME.format(version=Project.VERSION)
    MANIFEST_OUTPUT = BUILD / "manifest.json"
