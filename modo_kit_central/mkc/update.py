"""Update module for modo kit central."""
import json
from typing import Dict, List
from pathlib import Path
from urllib import request
from http import HTTPStatus

from .files import Paths
from .github import get_latest_release
from .prefs import KitData, KitManifest, GithubAsset


def kit_download(lpk_asset: GithubAsset) -> Path:
    """Download the lpk file from the given URL.

    Args:
        lpk_asset: The lpk asset from GitHub.

    Returns:
        The path to the downloaded lpk file.
    """
    # Pull the lpk file from the url.
    with request.urlopen(lpk_asset.url) as response:
        # Ensure the url is valid and the response is successful.
        if response.status == HTTPStatus.OK:
            # Get the path to the lpk file.
            lpk_path = Paths.KIT_DOWNLOADS / lpk_asset.name
            # Ensure the directory exists.
            lpk_path.parent.mkdir(parents=True, exist_ok=True)
            # Write the lpk file to disk.
            lpk_path.write_bytes(response.read())
            return lpk_path
        else:
            raise Exception(f"Failed to fetch lpk: {response.status}")


def get_assets(release_data: Dict) -> Dict[str, GithubAsset]:
    """Gets all assets from the given release data.

    Args:
        release_data: The release data from GitHub.

    Returns:
        A list of all the assets from the release data.
    """
    return {
        asset['name']: GithubAsset(
            name=asset['name'],
            size=asset['size'],
            url=asset['browser_download_url']
        ) for asset in release_data['assets']
    }


def get_manifest(manifest_asset: GithubAsset) -> KitManifest:
    """Fetch the manifest file from the given URL.

    Args:
        manifest_asset: The manifest asset from GitHub.

    Returns:
        The KitManifest dataclass containing the manifest data.
    """
    # Pull the manifest file from the url.
    with request.urlopen(manifest_asset.url) as response:
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
    release_data = get_latest_release(kit.repo)
    # Get the assets from the release data.
    assets = get_assets(release_data)
    # Get the manifest data to determine the correct lpk file to download.
    if 'manifest.json' not in assets:
        raise Exception("No manifest.json found in the release assets!")

    manifest_asset = assets['manifest.json']
    kit_manifest = get_manifest(manifest_asset)

    latest_lpk = assets.get(kit_manifest.latest, None)
    if not latest_lpk:
        raise Exception("No latest lpk found in the release assets!")

    lpk_file = kit_download(latest_lpk)
    print(lpk_file)
