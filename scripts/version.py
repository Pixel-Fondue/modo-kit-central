"""Handles writing to GitHubs environment file."""
import toml
import os


def set_env_vars() -> None:
    """Read version info from pyproject.toml and set GitHub environment variables."""
    data = toml.load("pyproject.toml")
    version = data['project']['version']
    name = data['project']['name']

    # GitHub Actions environment file
    with open(os.environ['GITHUB_ENV'], 'a') as env_file:
        env_file.write(f"KIT_VERSION={version}\n")
        env_file.write(f"KIT_NAME={name}\n")


if __name__ == '__main__':
    """Main entry point of the script."""
    set_env_vars()
