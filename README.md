# Modo Community Hub

The community hub is a kit for Modo that centralizes community information 
and third party kits into a singe, easy to use interface.

# Building or Installing the kit
Python version: `3.7` 

To install the kit to your appdata kits directory, run: `install.py`

To build the lpk file, run: `build.py`

# Current State
The current state of the kits is displaying Kits, Videos and some Social links.

# Future state
The hub will be designed as a UI that is easy to navigate showing various 
resources from the community, including: Various hard to find kits, Recent 
events in the Modo world, links to tutorials, links to all third-party kits 
with option to install directly from the hub given the developer has set up
there kit to do so.

# Publicly sourced information
After initial release, there will be a method for any user to submit their
kit/tutorial/blog or preset via GitHub. Walk-through tutorials are in the making
to help make the process easy for new users to GitHub.

# Creating A release
When A branch is merged to main, a GitHub action will begin to process the LPK 
generation and add the kit file to a release tag where users can download the latest file.