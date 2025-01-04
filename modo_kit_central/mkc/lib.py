import sys

from .prefs import Paths


def link_libs() -> None:
    """Links the proper libs folder based on the python version."""
    libs_root = Paths.KIT_ROOT / f"libs_{sys.version_info.major}{sys.version_info.minor}"
    if not f"{libs_root}" in sys.path:
        sys.path.append(f"{libs_root}")
        print(f"Added {libs_root} to sys.path")
