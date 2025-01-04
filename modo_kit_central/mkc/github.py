from typing import Dict, Any
import json
from urllib import parse

import requests
try:
    from PySide6.QtCore import QObject, Signal, qDebug
    from PySide6.QtGui import QPixmap
except ImportError:
    from PySide2.QtCore import QObject, Signal
    from PySide2.QtGui import QPixmap

from .prefs import URLS, Paths
from .utils import up_to_date
from .database import ManifestData

class ReleaseWorker(QObject):
    """Worker class to fetch the latest release from a repository."""
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, repo_url: str):
        super().__init__()
        self.repo_url = repo_url

    def run(self) -> None:
        """Runs the worker to fetch the latest release."""
        try:
            print("Fetching latest release...")
            release_info = get_latest_release(self.repo_url)
            self.finished.emit(release_info)
        except Exception as e:
            self.error.emit(f"Failed to fetch the latest release: {e}")


class DatabaseWorker(QObject):
    """Worker class to fetch the latest database."""
    finished = Signal()
    error = Signal(str)

    def __init__(self) -> None:
        """Initialization of the DatabaseWorker."""
        super().__init__()
        self.manifest: ManifestData = None
        self.manifest_data: Dict[str, Any] = None
        self.manifest_url: str = None
        self.database_url: str = None
        self.assets: Dict[str, Any] = None

    def run(self) -> None:
        """Runs the worker to fetch the latest database."""
        try:
            self.update_database()
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Failed to fetch the latest database: {e}")

    def update_database(self) -> None:
        release_data = get_latest_release(URLS.MODO_KIT_DATABASE)
        # Extract the assets from the release data.
        self.assets = {asset['name']: asset for asset in release_data['assets']}
        # Get the manifest data from the latest release.
        self.fetch_manifest()
        self.validate_version()

    def fetch_manifest(self) -> None:
        """Gets the manifest data from the latest release."""
        # Find the download url to the manifest.json file in the assets.
        self.manifest_url = self.assets.get('manifest.json', {}).get('browser_download_url', None)
        # Download the manifest.json data.
        self.manifest_data = requests.get(self.manifest_url).json()
        # Return the manifest data as a ManifestData object.
        self.manifest = ManifestData(**self.manifest_data)

    def fetch_database(self) -> None:
        """Retrieves the database file from the latest release."""
        # Get the url to the database file from the assets.
        self.database_url = self.assets.get(self.manifest.file, {}).get('browser_download_url', None)
        with requests.get(self.database_url) as response:
            # Write the database file to the resources' directory.
            Paths.DATABASE.write_bytes(response.content)

    def validate_version(self) -> None:
        """Validates the version of the database is up-to-date."""
        # Check if we have a local manifest file.
        if Paths.DATABASE_MANIFEST.exists():
            # Get the version from the local manifest file.
            version = json.loads(Paths.DATABASE_MANIFEST.read_text()).get('version', "0.0.0")
            # Check if the latest version is greater than the local version.
            if not up_to_date(version, self.manifest.version):
                # Download the database if the version is not up-to-date.
                self.fetch_database()
        else:
            # No local manifest file, download the database.
            self.fetch_database()

class AvatarWorker(QObject):
    """Worker class to fetch the author's avatar."""
    finished = Signal(QPixmap)
    error = Signal(str)

    def __init__(self, author: str):
        super().__init__()
        self.author = author

    def run(self) -> None:
        """Runs the worker to fetch the author's avatar."""
        try:
            avatar_pixmap = self.fetch_avatar()
            self.finished.emit(avatar_pixmap)
        except Exception as e:
            self.error.emit(f"Failed to fetch the author's avatar: {e}")

    def fetch_avatar(self) -> QPixmap:
        """Gets the author's avatar from the database."""
        # Ensure author name is URL safe.
        url_author_name = parse.quote(self.author)
        avatar_url = URLS.AUTHOR_AVATAR.format(author=url_author_name)
        with requests.get(avatar_url) as response:
            if response.status_code == 200:
                # Load the avatar image into a QPixmap object.
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
            else:
                raise Exception(f"Failed to fetch the author's avatar: {response.status_code}")

def get_latest_release_github(repo_url: str) -> Dict:
    """Gets the latest release manifest from the GitHub API.

    Args:
        repo_url: The URL to the repository.
    """
    owner_repo = repo_url.split(URLS.GITHUB_ROOT)[1]
    api_url = URLS.GITHUB_RELEASE_API.format(owner=owner_repo)
    with requests.get(api_url) as response:
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch the latest release: {response.status_code}")


def get_latest_release(repo_url: str) -> Dict:
    """Gets the latest database manifest file.

    Args:
        repo_url: The URL to the repository.
    """
    if URLS.GITHUB_ROOT in repo_url:
        return get_latest_release_github(repo_url)
    else:
        # TODO: Add support for other repository types.
        raise NotImplementedError("Only GitHub repositories are supported at this time.")
