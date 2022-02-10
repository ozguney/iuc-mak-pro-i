import os

def GetGpxFolderPath():
    path = os.path.realpath(__file__)           # C:\Users\OZGUN\Documents\GitHub\iuc-mak-pro-i\src\_filemanagement.py
    dir = os.path.dirname(path)                 # C:\Users\OZGUN\Documents\GitHub\iuc-mak-pro-i\src
    dir = dir.replace("src", "gpx_files")       # Changing directory from src to gpx_files
    return dir                                  # C:\Users\OZGUN\Documents\GitHub\iuc-mak-pro-i\gpx_files

def GetDocsFolderPath():
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace("src", "docs")
    return dir