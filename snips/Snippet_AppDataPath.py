# Get the Local AppData path

import os

PathSeparator = "/"


def GetAppDataEnv():
    ModoPath = os.getenv('APPDATA')
    # print(ModoPath)
    return ModoPath


# print(GetAppDataEnv())

if GetAppDataEnv() != None and os.path.lexists(GetAppDataEnv()):
    print('Good we got the AppData Path')


def valid_SlackPath():
    if GetAppDataEnv() != None and os.path.lexists(GetAppDataEnv()):
        AppDataPath = os.path.splitext(GetAppDataEnv())
        print(AppDataPath)
        return AppDataPath


print(valid_SlackPath())

###### MUCH FASTER
# python2:
from os import path

print(path.expanduser("~\\appdata"))
# python3:
from pathlib import Path

print(Path("~\\appdata").expanduser())
