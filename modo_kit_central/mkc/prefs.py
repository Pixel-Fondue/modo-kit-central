import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .gui import KitCentralWindow


@dataclass
class KitInfo:
    """Dataclass for the kit's information."""
    name: str
    enabled: bool
    version: str
    path: Path


@dataclass
class ImportInfo:
    """Dataclass for the import information."""
    name: str
    version: str
    path: Path


@dataclass
class DATA:
    """Dataclass for storing live data while the kit is running."""
    local: bool = False
    resources: Path = None
    authors: Dict = None
    CSS: str = ""
    mkc_window: 'KitCentralWindow' = None
    modo_kits: Dict[str, KitInfo] = None


class Paths:
    """Paths for Modo Kit Central resources."""
    KIT_ROOT = Path(__file__).parent.parent.absolute()
    RESOURCES = KIT_ROOT / "resources"
    DATABASE = RESOURCES / "kits.db"
    IMAGES = RESOURCES / "images"
    ICON = IMAGES / "icon.png"
    IMAGES_CSS = IMAGES / "css"
    BANNERS = IMAGES / "banners"
    BANNER_MKC = BANNERS / "Modo Kit Central.png"


class Text:
    """Dataclass for storing text information."""
    title = "Modo Kit Central"
    author = "Author: <a href='{}' style='color: white'>{}</a>"
    lbl_link = "<a href='{link}' style='color: white'>{text}</a>"
    info_block = (
        "Welcome to Modo Kit Central! aka MKC\n\n"
        "MKC is a tool to help you find and install kits for Modo."
        "Currently, MKC only supports free kits. If you are a Kit Author that"
        "would like to onboard your kits, Reach out to PF for more info."
        "Pixel Fondue is working hard"
        "to onboard paid kits as well. Stay tuned for updates!"
    )


class KEYS:
    """Keys for the different tabs."""
    KITS = "Kits"
    AUTHORS = "Authors"
    INFO = "Info"


class KIT:
    """Constants for the Kit Central."""
    ABV = "mkc"
    NAME = "modo_kit_central"
    NICE_NAME = "Modo Kit Central"
    CMD_LAUNCHER = f"{ABV}.launcher"


@dataclass
class KitData:
    """Dataclass for the kit's information."""
    id: int
    name: str
    label: str
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


@dataclass
class QueryData:
    """Dataclass for the query data."""
    SelectKits: str = "SELECT * FROM kits WHERE TRUE"
    SearchTerm: str = " AND (name LIKE ? OR author LIKE ? OR search LIKE ? OR Description LIKE ?)"
    SelectAuthor: str = "SELECT * FROM authors WHERE name LIKE ?"
    SelectKitsByAuthor: str = "SELECT * FROM kits WHERE author = ?"
