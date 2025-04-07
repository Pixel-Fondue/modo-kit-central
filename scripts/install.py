import sys
import shutil
from pathlib import Path

from .prefs import Paths, Project


def install() -> None:
    """Installs the development kit into the modo kits directory.

    Raises:
        ValueError: If the platform is not supported.
    """
    # Get the os dependant kits path
    if sys.platform == "win32":
        install_path = Path(r"~\AppData\Roaming\Luxology\Kits").expanduser()
    elif sys.platform == "darwin":
        install_path = Path("~/Library/Application Support/Luxology/Kits").expanduser()
    else:
        raise ValueError(f"Unsupported platform: {sys.platform}")

    # Get the modo install path for kit
    modo_kit_path = install_path / Project.NAME

    # If the Kit exists in the modo kit path, remove it before copying the new one.
    if modo_kit_path.exists():
        print("Removing old kit...")
        shutil.rmtree(modo_kit_path)

    print("Copying new kit data...")
    # Copy the development kit to the modo kit path.
    shutil.copytree(src=Paths.KIT, dst=modo_kit_path)
    print("Installation complete.")


def main() -> None:
    """Main entry point of the installer script."""
    install()


if __name__ == '__main__':
    """Module entry point of the script."""
    main()
