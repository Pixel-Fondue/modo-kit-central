"""Core data and types for Modo Kit Central."""
import sys
import json
from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .gui import KitCentralWindow


@dataclass
class KitInfo:
    """Dataclass for the kit's information."""
    name: str       # The name of the kit.
    enabled: bool   # If the kit is enabled.
    version: str    # The version of the kit.
    path: Path      # The path to the kits root directory.


@dataclass
class ImportInfo:
    """Dataclass for the import information."""
    name: str       # The name of the kit.
    version: str    # The version of the kit.
    path: Path      # The path to the kits root directory.


@dataclass
class DATA:
    """Dataclass for storing live data while the kit is running."""
    local: bool = False
    resources: Path = None
    authors: Dict = None
    CSS: str = ""
    mkc_window: 'KitCentralWindow' = None
    modo_kits: Dict[str, KitInfo] = None
    local_kits: Dict[str, KitInfo] = None


@dataclass
class URLS:
    """Dataclass for storing URL information."""
    GITHUB_ROOT = "github.com/"
    MODO_KIT_DATABASE = "https://github.com/Pixel-Fondue/modo-kit-database"
    GITHUB_RELEASE_API = "https://api.github.com/repos/{owner}/releases/latest"
    AUTHOR_AVATAR = "https://raw.githubusercontent.com/Pixel-Fondue/modo-kit-database/refs/heads/main/kits/{author}/avatar.png"


@dataclass
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


@dataclass
class KEYS:
    """Keys for the different tabs."""
    KITS = "Kits"
    AUTHORS = "Authors"
    INFO = "Info"


@dataclass
class KIT:
    """Constants for the Kit Central."""
    ABV = "mkc"
    NAME = "modo_kit_central"
    NICE_NAME = "Modo Kit Central"
    CMD_LAUNCHER = f"{ABV}.launcher"


@dataclass
class KitManifest:
    """Dataclass to hold information from a manifest.json file for a kit."""
    name: str               # The name of the kit.
    version: str            # The version of the kit.
    description: str        # The description of the kit.
    # Optional
    latest: str = None      # The latest lpk filename for all platforms.
    latest_win: str = None  # The latest lpk filename for Windows.
    latest_mac: str = None  # The latest lpk filename for Mac.

    def __post_init__(self) -> None:
        """Get the latest lpk for the active platform."""
        if self.latest:
            # If latest is used, assume it's the latest for all platforms.
            return
        elif sys.platform == "win32":
            self.latest = self.latest_win
        elif sys.platform == "darwin":
            self.latest = self.latest_mac


@dataclass
class GithubAsset:
    """Dataclass to hold information from a GitHub release."""
    name: str   # The name of the asset.
    size: int   # The size of the asset.
    url: str    # The URL to download the asset.


@dataclass
class KitData:
    """Dataclass for the kit's information."""
    id: int             # The id of the kit within the database.
    name: str           # The name attribute from the index.cfg.
    label: str          # The nice name of the kit to display.
    author: str         # The original author of the kit.
    version: str        # The current version of the kit.
    description: str    # The description of the kit for users.
    search: List[str]   # The search terms for the kit.
    # The following fields are optional.
    url: str = None             # The URL to the kit's homepage.
    help: str = None            # The URL to the kit's help page.
    repo: str = None            # The URL to the GitHub repo for the kit installation.
    has_banner: bool = False    # If the kit has a banner image.
    installable: bool = False   # If the kit is installable via MKC.

    # Search will come in as a comma separated string, so we need to convert it to a list.
    def __post_init__(self) -> None:
        """Convert the search string to a list."""
        self.search = self.search.split(",") if self.search else []


@dataclass
class AuthorData:
    """Dataclass for the author's information."""
    id: int     # The id of the author within the database.
    name: str   # The name of the author.
    # The following fields are optional.
    avatar: bool = False            # Whether the author has an avatar to display.
    handle: str = None              # The author's handle.
    links: Dict[str, str] = None    # A JSON object containing links to the author's social media.

    def __post_init__(self):
        """Convert the links json string to a dictionary."""
        if self.links is not None:
            self.links = json.loads(self.links) if self.links else {}


@dataclass
class QueryData:
    """Dataclass for the query data."""
    SelectKits: str = "SELECT * FROM kits WHERE TRUE"
    SearchTerm: str = " AND (name LIKE ? OR author LIKE ? OR search LIKE ? OR Description LIKE ?)"
    SelectAuthor: str = "SELECT * FROM authors WHERE name LIKE ?"
    SelectKitsByAuthor: str = "SELECT * FROM kits WHERE author = ?"


@dataclass
class TabRequest:
    """Dataclass for a tab opening request."""
    type: str               # The type of tab to open.
    name: str = None        # The name of the tab.
    show: bool = False      # If the tab should be shown.
    closeable: bool = True  # If the tab is closeable.
    kwargs: Dict = None     # The kwargs to pass to the tab.


class KitAction(Enum):
    """Enum for a kits action button."""
    NONE = "none"
    INSTALL = "install"
    UPDATE = "update"
    UNINSTALL = "uninstall"
