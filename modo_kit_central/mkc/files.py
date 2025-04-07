from os import environ
from sys import platform
from dataclasses import dataclass
from pathlib import Path


def get_cache_dir() -> Path:
    """Get the platform-specific cache directory.

    Returns:
        Path to the cache directory.
    """
    if platform == "win32":
        # Windows: AppData/Local/ModoKitCentral/cache
        cache_dir = Path("~/AppData/Local").expanduser() / "ModoKitCentral"
    elif platform == "darwin":
        # macOS: ~/Library/Caches/ModoKitCentral
        cache_dir = Path.home() / "Library" / "Caches" / "ModoKitCentral"
    else:
        # Fallback to Linux: ~/.cache/ModoKitCentral
        cache_dir = Path.home() / ".cache" / "ModoKitCentral"

    # Ensure the directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


@dataclass(frozen=True)
class Paths:
    """Paths for Modo Kit Central resources."""
    KIT_ROOT = Path(__file__).parent.parent.absolute()
    KIT_LIBS = KIT_ROOT / f"libs"
    RESOURCES = KIT_ROOT / "resources"
    DATABASE = RESOURCES / "mkc_kits.db"
    DATABASE_MANIFEST = RESOURCES / "manifest.json"
    TEST_RELEASE = RESOURCES / "test_release.json"
    AVATAR = RESOURCES / "avatars" / "profile.png"
    IMAGES = RESOURCES / "images"
    ICON = IMAGES / "icon.png"
    IMAGES_CSS = IMAGES / "css"
    BANNERS = IMAGES / "banners"
    BANNER_MKC = BANNERS / "Modo Kit Central.png"
    # Installer paths.
    KIT_CACHE = get_cache_dir()
    KIT_DOWNLOADS = KIT_CACHE / "kits"
