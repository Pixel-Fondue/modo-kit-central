from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Paths:
    """All paths related to building the project."""
    ROOT = Path(__file__).parent.parent.absolute()
    # Kit paths
    KIT = ROOT / "modo_kit_central"
    KIT_RESOURCES = KIT / "resources"
    KIT_DATABASE = KIT_RESOURCES / "kits.db"
    # Tooling paths
    SCRIPTS = ROOT / "scripts"
    SCRIPTS_RESOURCES = SCRIPTS / "resources"
    SCRIPT_QUERIES = SCRIPTS / "queries"
    # Data paths
    KIT_DATA = SCRIPTS_RESOURCES / "kits.json"
    AUTHOR_DATA = SCRIPTS_RESOURCES / "authors.json"
