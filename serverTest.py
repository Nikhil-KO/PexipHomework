import os
import shutil
import string
import random
import pathlib
import unittest
from server.dropboxService import DropBoxService


dropbox : DropBoxService = None
letters = string.ascii_lowercase

# Mimic the flask FileStorage object to write
class FakeFileStorage:
    
    def __init__(self, path : pathlib.Path) -> None:
        self.path = path

    @staticmethod
    def save(file_path):
        with open(file_path, 'w') as f:
            print("Unit test written data", file=f, end='')

class ServerUnitTests(unittest.TestCase):

    def test_create_dir(self):
        folder_name = ''.join(random.choice(letters) for i in range(10))
        dropbox.create_directory(folder_name)
        self.assertTrue(os.path.exists(os.path.join(dropbox._dir_loc, folder_name)), "Failed to create folder")
        return folder_name

    def test_create_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        file_path = os.path.join(dropbox._dir_loc, file_name)
        file = FakeFileStorage(file_path)
        dropbox.create_file(file_name, file)
        self.assertTrue(os.path.exists(file_path), "Failed to create file")
        with open(file_path, 'r') as f:
            self.assertEqual("Unit test written data", f.read(), "File created with wrong data")
        return file_name
    
    def test_modify_file(self):
        file_name = self.test_create_file()
        dropbox.modify_file(file_name, str.encode("Modified data test"))
        file_path = os.path.join(dropbox._dir_loc, file_name)
        with open(file_path, 'r') as f:
            self.assertEqual("Modified data test", f.read(), "File modifed with wrong data")

    def test_delete_directory(self):
        dir_name = self.test_create_dir()
        dir_path = os.path.join(dropbox._dir_loc, dir_name)
        self.assertTrue(os.path.exists(dir_path), "Failed to create directory")
        dropbox.delete_directory(dir_name)
        self.assertTrue(not os.path.exists(dir_path), "Failed to delete directory")

    def test_delete_file(self):
        file_name = self.test_create_file()
        file_path = os.path.join(dropbox._dir_loc, file_name)
        self.assertTrue(os.path.exists(file_path), "Failed to create file")
        dropbox.delete_file(file_name)
        self.assertTrue(not os.path.exists(file_path), "Failed to delete file")
    
    def test_move_dir(self):
        dir_name = self.test_create_dir()
        dir_path = os.path.join(dropbox._dir_loc, dir_name)
        self.assertTrue(os.path.exists(dir_path), "Failed to create directory")
        new_dir_name = ''.join(random.choice(letters) for i in range(10))
        new_dir_path = os.path.join(dropbox._dir_loc, new_dir_name)
        dropbox.move(dir_name, new_dir_name)
        self.assertTrue(not os.path.exists(dir_path), "Failed to move directory, old one still present")
        self.assertTrue(os.path.exists(new_dir_path), "Failed to move directory, new one not present")

    def test_move_file(self):
        file_name = self.test_create_file()
        file_path = os.path.join(dropbox._dir_loc, file_name)
        self.assertTrue(os.path.exists(file_path), "Failed to create file")
        new_file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        new_file_path = os.path.join(dropbox._dir_loc, new_file_name)
        dropbox.move(file_name, new_file_name)
        self.assertTrue(not os.path.exists(file_path), "Failed to move file, old one still present")
        self.assertTrue(os.path.exists(new_file_path), "Failed to move file, new one not present")


def run():
    print("\nRunning server tests")
    root_dir = pathlib.Path('tests/server_data/')
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    global dropbox
    dropbox = DropBoxService(root_dir)
    unittest.main(exit=False)
    shutil.rmtree(root_dir)
    print("completed running server tests")
    

if __name__ == "__main__":
    run()