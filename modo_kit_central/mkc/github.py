from typing import Dict, Any
import json

import requests
from PySide6.QtCore import QObject, Signal

from .prefs import URLS, Paths

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
    latest_release: Dict[str, Any]
    assets: Dict[str, Dict[str, Any]]

    def __init__(self) -> None:
        """Initialization of the DatabaseWorker."""
        super().__init__()

    def run(self) -> None:
        """Runs the worker to fetch the latest database."""
        try:
            self.update_database()
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Failed to fetch the latest database: {e}")

    def update_database(self) -> None:
        print("Fetching latest database...")
        self.latest_release = get_latest_release(URLS.MODO_KIT_DATABASE)
        # Store the latest release for debugging.
        # Paths.TEST_RELEASE.write_text(json.dumps(self.latest_release, indent=2))
        self.mark_assets()
        # self.validate_version()
        # self.download_database()

    def mark_assets(self) -> None:
        """Marks the assets as downloaded."""
        # Store the assets in a dictionary for easy access.
        self.assets = {asset['name']: asset for asset in self.latest_release['assets']}
        self.manifest = self.assets.get("manifest.json", None)
        self.manifest_url = self.manifest.get("browser_download_url", None)
        # Read the json from the manifest file.
        print(self.manifest_url)
        manifest = requests.get(self.manifest_url).json()
        print(manifest)


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
