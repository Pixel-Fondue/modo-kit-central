"""Update module for modo kit central."""
import json
from pathlib import Path
from urllib import request
from http import HTTPStatus

from .github import get_latest_release
from .prefs import KitData, KitManifest


def kit_download(lpk_url: str) -> Path:
    """Download the lpk file from the given URL.

    Args:
        lpk_url: The URL to the lpk file.

    Returns:
        The path to the downloaded lpk file.
    """
    ...


def get_manifest(manifest_url: str) -> KitManifest:
    """Fetch the manifest file from the given URL.

    Args:
        manifest_url: The URL to the manifest file.

    Returns:
        The KitManifest dataclass containing the manifest data.
    """
    # Pull the manifest file from the url.
    with request.urlopen(manifest_url) as response:
        # Ensure the url is valid and the response is successful.
        if response.status == HTTPStatus.OK:
            # Load the manifest data from the response.
            manifest_data = json.loads(response.read().decode())
            # Unpack the manifest data into the KitManifest dataclass.
            return KitManifest(**manifest_data)
        else:
            raise Exception(f"Failed to fetch manifest: {response.status}")


def update_kit(kit: KitData) -> None:
    """Update the given kit.

    Args:
        kit: The kit to update.
    """
    # Check if there is a manifest file url for the kit.
    if not kit.repo:
        raise Exception("Repo not set, cannot update kit!")

    # Get the latest release information for the kit.
    release = get_latest_release(kit.repo)

    # Get the manifest file.
    manifest_release_data = next(m for m in release['assets'] if m['name'] == 'manifest.json')
    manifest_url = manifest_release_data['browser_download_url']
    # Get the lpk from the release data.
    # TODO: os specific packages?
    print(manifest_url)
    manifest = get_manifest(manifest_url)
    print(manifest)
