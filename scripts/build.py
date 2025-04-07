from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED

from .utils import make_index, readable_size, set_version
from .prefs import Paths, Project


def create_manifest() -> None:
    """Creates the manifest.json file for the published kit."""
    ...


def package_kit() -> Path:
    """Packages the kit into an LPK file.

    Returns:
        lpk_path: The path to the LPK file.
    """

    # Get all files in the kit directory while ignoring .pyc files
    kit_files = [f for f in Paths.KIT.glob("**/*") if f.is_file() and not f.suffix == ".pyc"]

    # Clear the build directory
    if Paths.BUILD.exists():
        rmtree(Paths.BUILD)
    # Remake the build directory
    Paths.BUILD.mkdir(parents=True, exist_ok=True)

    # Set the version.py file to the version number
    set_version(Project.VERSION)

    # Message to display to the users
    user_message = f"Successfully installed {Project.NAME}: v{Project.VERSION}"

    # Build the LPK file.
    with ZipFile(Paths.LPK_OUTPUT, mode='w', compression=ZIP_DEFLATED) as lpk:
        # Add the license
        lpk.write(Paths.LICENSE, Paths.ZIP_LICENSE)
        # Generate the index.xml file data
        index_data = make_index(folder=Paths.KIT, files=kit_files, message=user_message)
        # Write the index.xml file
        lpk.writestr(Paths.ZIP_INDEX, index_data)

        # Write all file into the lpk
        for file in kit_files:
            print(f"Adding: {file.relative_to(Paths.KIT)}")
            lpk.write(file, file.relative_to(Paths.KIT).as_posix())

    # Get the size of the LPK file, in MB
    package_size = readable_size(Paths.LPK_OUTPUT.stat().st_size, decimal=2)

    print(f"\nLPK package built: {Paths.LPK_OUTPUT}")
    print(f"Package Size: {package_size}")
    return Paths.LPK_OUTPUT


def main():
    """Main entry point of the builder script."""
    package_kit()


if __name__ == '__main__':
    """Module entry point of the script."""
    main()
