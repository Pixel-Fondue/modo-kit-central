import os

import toml

from .prefs import Paths

def install_libs():
    print("Installing required libraries...")
    project = toml.load("pyproject.toml")
    poetry = project.get('tool', {}).get('poetry', {})
    # Install the required libraries for the kit.
    kit_dependencies = poetry.get('group').get('kit').get('dependencies', {})
    os.system(f"python -m pip install {' '.join(kit_dependencies)} -t {Paths.KIT_LIBS_310}")
    print("Done.")



if __name__ == '__main__':
    install_libs()
