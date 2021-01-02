import os
import shutil
import pathlib

class DropBoxService:
    
    def __init__(self, dir_loc : pathlib.Path) -> None:
        self._dir_loc = dir_loc
    
    def create_directory(self, new_dir : str):
        new_dir = os.path.join(self._dir_loc, new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    def create_file(self, new_path : str, data):
        new_file_path = os.path.join(self._dir_loc, new_path)
        data.save(new_file_path)
    
    def modify_file(self, path : str, data):
        file_path = os.path.join(self._dir_loc, path)
        # TODO 
        # safety check
        # if not os.path.exists(file_path):
        with open(file_path, 'wb') as file:
            file.write(data)

    def delete_file(self, path : str):
        file_path = os.path.join(self._dir_loc, path)
        os.remove(file_path)

    def delete_directory(self, path : str):
        dir_path = os.path.join(self._dir_loc, path)
        shutil.rmtree(dir_path)
        