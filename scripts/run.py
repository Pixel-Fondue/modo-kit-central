import sys
from os import environ
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


def link_kit() -> None:
    """Links the mkc library to the sys path."""
    repo_dir = Path().absolute()
    mkc_path = repo_dir / "modo_kit_central"
    sys.path.append(str(mkc_path))


def run() -> None:
    """Runs the mkc library."""
    from mkc.gui import KitCentralWindow
    from mkc.prefs import DATA, KitInfo

    mkc_app = QApplication(sys.argv)
    mkc_app.setAttribute(Qt.AA_EnableHighDpiScaling)

    # Load mock kit data
    DATA.modo_kits = {
        'MODO_KIT_CENTRAL': KitInfo(
            name="MODO_KIT_CENTRAL", version="0.0.0", enabled=True, path=Path()
        ),
    }
    DATA.mkc_window = KitCentralWindow()

    sys.exit(mkc_app.exec())


def main():
    """Main entry point of the runner script."""
    # Add mck to the sys path
    link_kit()
    # Enable local mode
    environ['MKC_LOCAL'] = 'True'
    # Run MKC gui
    run()


if __name__ == '__main__':
    main()
