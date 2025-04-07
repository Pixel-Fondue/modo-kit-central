"""Handles writing to GitHubs environment file."""
import os

from .prefs import Project


def set_env_vars() -> None:
    """Read version info from pyproject.toml and set GitHub environment variables."""

    # GitHub Actions environment file
    with open(os.environ['GITHUB_ENV'], 'a') as env_file:
        env_file.write(f"KIT_VERSION={Project.VERSION}\n")
        env_file.write(f"KIT_NAME={Project.NAME}\n")


if __name__ == '__main__':
    """Main entry point of the script."""
    set_env_vars()
