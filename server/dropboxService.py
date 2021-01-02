import os
import shutil
import pathlib

# Class to recreate file system changes on client here on server side
class DropBoxService:
    
    def __init__(self, dir_loc : pathlib.Path) -> None:
        self._dir_loc = dir_loc
    
    def create_directory(self, new_dir : str):
        new_dir = os.path.join(self._dir_loc, new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    def create_file(self, new_path : str, data):
        new_file_path = os.path.join(self._dir_loc, new_path)
        file_dir = os.path.dirname(pathlib.Path(new_file_path))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        data.save(new_file_path)
    
    def modify_file(self, path : str, data):
        file_path = os.path.join(self._dir_loc, path)
        # safety check
        if not os.path.exists(file_path):
            self.create_file(path, data)
            return
        with open(file_path, 'wb') as file:
            file.write(data)

    def delete_file(self, path : str):
        file_path = os.path.join(self._dir_loc, path)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def delete_directory(self, path : str):
        dir_path = os.path.join(self._dir_loc, path)
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
    
    def move(self, path_from : str, path_to : str):
        path_from = os.path.join(self._dir_loc, path_from)
        path_to = os.path.join(self._dir_loc, path_to)
        shutil.move(path_from, path_to)