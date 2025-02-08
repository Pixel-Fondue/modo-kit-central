from .prefs import Paths, DATA


def set_absolute_images(css_data: str) -> str:
    """Sets the absolute path for images in the CSS.

    Args:
        css_data: The CSS data to update.
    """
    return css_data.replace("url(", f"url({Paths.IMAGES_CSS.as_posix()}/")


def load_stylesheet() -> None:
    """Leads the stylesheet used for the QT widgets."""
    style_path = Paths.RESOURCES / "style.css"
    # Load the css file into the data object.
    DATA.CSS = set_absolute_images(style_path.read_text())

    if DATA.local:
        # Load CSS from repo resources
        repo_resources = Paths.KIT_ROOT.parent / "scripts" / "resources"
        repo_style_path = repo_resources / "style.css"
        # pre-pend css data to the kit css data
        DATA.CSS = set_absolute_images(repo_style_path.read_text()) + DATA.CSS


def up_to_date(version_local: str, version_latest: str) -> bool:
    """Compares two version strings.

    Args:
        version_local: The local version string.
        version_latest: The latest version string.
    """
    try:
        local_version = [int(v) for v in version_local.split(".")]
        latest_version = [int(v) for v in version_latest.split(".")]
    except ValueError:
        # Version is corrupted, assume it's out-of-date, update required.
        return False

    if local_version < latest_version:
        # Local version is out-of-date, update required.
        return False
    else:
        # Local version is up-to-date.
        return True


def debug():
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=6000, stdoutToServer=True, stderrToServer=True)