import os
import sys
import time
import requests
import pathlib


def scan(root_path : pathlib.Path):
    pass

def init_client(root_path : pathlib.Path):
    folders = []
    file_details = {}
    for path, _, files in os.walk(root_path):
        folders.append(path)
        for file in files:
            stats = os.stat(os.path.join(path, file))
            file_details[stats.st_ino] = stats
    return folders, file_details

def main():
    
    DATA_DIR = "client/listen/"
    root_path = pathlib.Path(DATA_DIR).absolute()

    folders, file_details = init_client(root_path)
    scan(root_path, folders, file_details)

if __name__ == "__main__":
    main()