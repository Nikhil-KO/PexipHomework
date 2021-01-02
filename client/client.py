import os
import time
import pathlib
from observer import Observer
from dispatcher import Dispatcher

SLEEP_CONSTANT = 2.5
dispatcher : Dispatcher = None
DATA_DIR = "listen/"

def on_modify(path: pathlib.Path):
    file_path = os.path.join(DATA_DIR, path)
    with open(file_path, 'rb') as f:
        dispatcher.modify_file(path, f)
    print("modified ", str(path))

def on_move(path_from : pathlib.Path, path_to : pathlib.Path):
    dispatcher.move(str(path_from), str(path_to))
    print("moved ", str(path_from), " to ", str(path_to))

def on_create(path : pathlib.Path, directory : bool):
    if (directory):
        dispatcher.create_directory(str(path))
    else:
        file_path = os.path.join(DATA_DIR, path)
        with open(file_path, 'rb') as f:
            dispatcher.create_file(path, f)
    print("new ", str(path))

def on_delete(path : pathlib.Path, directory : bool):
    dispatcher.delete(path, directory)
    print("deleted ", str(path))

def scan(root_path : pathlib.Path, folders, file_details, ):
    observer = Observer(root_path, folders, file_details, on_modify, on_move, on_create, on_delete)
    while True:
        observer.watch()
        time.sleep(SLEEP_CONSTANT)
    

def init_client(root_path : pathlib.Path):
    folder_details = {}
    file_details = {}
    for path, _, files in os.walk(root_path):
        folder_stats = os.stat(path)
        folder_details[folder_stats.st_ino] = [folder_stats, pathlib.Path(path).relative_to(root_path)]
        for file in files:
            file_path = pathlib.Path(os.path.join(path, file))
            stats = os.stat(file_path)
            file_details[stats.st_ino] = [stats, file_path.relative_to(root_path)]
    return folder_details, file_details

def main():
    
    root_path = pathlib.Path(DATA_DIR)

    folder_details, file_details = init_client(root_path)
    print(folder_details)
    print("-----------")
    print(file_details)
    global dispatcher
    dispatcher = Dispatcher('http://127.0.0.1:5000/')

    scan(root_path, folder_details, file_details)

if __name__ == "__main__":
    main()