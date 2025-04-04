# Local setup:
___
This repository uses `poetry` to handle the dependencies.
The following steps will help you set up the project locally.
1. Clone the repository.
2. Use poetry to install the dependencies.
   - `poetry install`
3. Activate the virtual environment.
   - `poetry shell`
4. Command to remove the .venv folder.
   - `poetry env remove`


# Python setup using pyenv:
___
It is preferred to use `pyenv` to manage python installations on your machine.

MacOS: 
- `brew install pyenv`
- `pyenv install 3.10.11`
- `pyenv global 3.10.11`

Windows:
- `choco install pyenv-win`
- `pyenv install 3.10.11`
- `pyenv global 3.10.11`
- Without choco:
- - Follow the instructions on the [pyenv-win github page](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#powershell).

# Running the scripts
1. Install the kit locally.
   - `python -m scripts.install`
   - `poetry run install`
2. Build the .lpk file.
   - `python -m scripts.build`
   - `poetry run build`
3. Run the UI locally. (Not in modo)
   - `python -m scripts.run`
   - `poetry run app`


# Debugging
The kit is designed to be able to run inside and outside Modo. If you need to run the remote debugger, here is the setup:
- PyCharm
  - Install PyCharms' debugger into the kits lib folder. (Requires pro)
      - `pip install -t modo_kit_central/libs pydevd-pycharm~=<PYCHARM_VERSION>`
  - Install the kit.
    - `python -m scripts.install`
    - `poetry run install`
  - Create a debug server in PyCharm.
    - Go to `Run` -> `Edit Configurations`
    - Click the `+` in the top left and select `Python Debug Server`
    - Set the port to `6001`
  - Set up the local and remote paths in the debugger.
    - Local: `$PROJECT_DIR$/modo_kit_central/mkc`
    - Remote: `C:/Users/USERNAME/AppData/Roaming/Luxology/Kits/modo_kit_central/mkc`
  - Run the debugger in pycharm.
  - Run the kit command to link the debugger.
    - `mkc.debug 6001`
  - You should then see the debugger connect in PyCharm.
- VSCode
  - `TODO`

## TODO List:
- [ ] Clean up kit JSON data.
- [ ] Add more kits to the kits.json file.
- [ ] Create workflow for adding a new kit.
- [ ] Allow self update of the hub.
- [ ] Show installed kits.
