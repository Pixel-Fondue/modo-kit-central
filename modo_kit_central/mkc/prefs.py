import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .gui import KitCentralWindow


@dataclass
class DATA:
    local: bool = False
    resources: Path = None
    authors: dict = None
    CSS: str = ""
    mkc_window: 'KitCentralWindow' = None


class Paths:
    KIT_ROOT = Path(__file__).parent.parent.absolute()
    RESOURCES = KIT_ROOT / "resources"
    IMAGES = RESOURCES / "images"
    IMAGES_CSS = IMAGES / "css"
    DATABASE = RESOURCES / "kits.db"


class Text:
    title = "Modo Kit Central"
    author = "Author: <a href='{}' style='color: white'>{}</a>"
    lbl_link = "<a href='{link}' style='color: white'>{text}</a>"


class KEYS:
    KITS = "kits"
    AUTHORS = "authors"


class KIT:
    ABV = "mkc"
    NAME = "modo_kit_central"
    NICE_NAME = "Modo Kit Central"
    CMD_LAUNCHER = f"{ABV}.launcher"


@dataclass
class KitData:
    """Dataclass for the kit's information."""
    id: int
    name: str
    author: str
    version: str
    description: str
    url: str
    help: str
    installable: bool
    search: List[str]

    # Search will come in as a comma separated string, so we need to convert it to a list.
    def __post_init__(self) -> None:
        """Convert the search string to a list."""
        self.search = self.search.split(",") if self.search else []


@dataclass
class AuthorData:
    """Dataclass for the author's information."""
    id: int
    name: str
    avatar: str
    handle: str
    links: Dict[str, str]

    def __post_init__(self):
        """Convert the links json string to a dictionary."""
        self.links = json.loads(self.links) if self.links else {}
