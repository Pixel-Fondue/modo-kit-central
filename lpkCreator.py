"""
This helps generate the index.xml file you need to unpack a kit using the .lpk installers.
Fill in the Setup Variables below, and the index.xml file will show up in your kit directory.
"""

import os
from os import path

# Setup Variables for Kit
kitFolder = path.join(path.dirname(__file__), "community_hub")
kitName = "Modo_Community_Hub"
kitMessage = "%s Kit - v1.13 installation complete. Best regards, Franck Elisabeth" % kitName
modoVersion = "1000"
installAlias = "kit"


def listFiles(kitPath):
    """
    Takes a directory to your kit and scans for files to be unpacked by the lpk file
    """
    files = []
    for r, d, f in os.walk(kitFolder):
        for n in f:
            if '.DS_Store' not in n:
                files.append(os.path.join(r, n).replace(kitFolder, '').replace('\\', '/'))
    return files


def buildIndexText(kitName, targetDir, files, kitMessage, modoVersion):
    """
    Creates a string to be written to the index.xml
    """
    # Headers
    tmp = '<?xml version="1.0" encoding="utf-8"?>\n<package version="%s">' % modoVersion
    # Kit Name and Restart option
    tmp += ('\n\t<%s name="%s" restart="YES">' % (targetDir, kitName))
    for i in files:
        # Append each file to unpack
        tmp += ('\n\t\t<source target="%s%s">%s</source>' % (kitName, i, i[1:]))
    tmp += ('\n\t</%s>\n\t<message button="Help">%s</message>\n</package>' % (targetDir, kitMessage))
    return tmp


# Main execution
files = listFiles(kitFolder)
index = buildIndexText(kitName, installAlias, files, kitMessage, modoVersion)
f = open(os.path.join(kitFolder, "index.xml"), "w+")
f.write(index)
f.close()
