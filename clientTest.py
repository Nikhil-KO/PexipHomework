import os
import time
import shutil
import string
import random
import pathlib
import unittest
import threading
from client.observer import Observer

class FakeHandler:

    def __init__(self) -> None:
        self.created = None
        self.modified = None
        self.moved = None
        self.deleted = None

    def on_create(self, path : pathlib.Path, directory : bool):
        self.created = path

    def on_modify(self, path: pathlib.Path):
        self.modified = path

    def on_move(self, path_from : pathlib.Path, path_to : pathlib.Path):
        self.moved = (path_from, path_to)

    def on_delete(self, path : pathlib.Path, directory : bool):
        self.deleted = path

test_completed : bool = False
SLEEP_CONSTANT : float = 2
fake_handler : FakeHandler = None
root_dir : pathlib.Path = pathlib.Path('tests/listen/')
letters = string.ascii_lowercase

class ClientUnitTests(unittest.TestCase):
    
    def test_create_dir(self):
        folder_name = ''.join(random.choice(letters) for i in range(10))
        path = pathlib.Path(folder_name)
        test_folder = os.path.join(root_dir, path)
        os.makedirs(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(fake_handler.created), str(path), "Observer did not pick up directory being made")
        return path

    def test_create_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        path = pathlib.Path(file_name)
        test_file = os.path.join(root_dir, path)
        with open(test_file, 'w') as f:
            print("unit test file", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(fake_handler.created), str(path), "Observer did not pick up file being made")
        return path

    def test_modify_file(self):
        path = self.test_create_file()
        test_file = os.path.join(root_dir, path)
        # modify contents
        with open(test_file, 'w') as f:
            print("modifed text", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(fake_handler.modified), str(path), "Observer did not pick up file being modified")

    def test_move_dir(self):
        path = self.test_create_dir()
        test_folder = os.path.join(root_dir, path)
        # move folder
        new_folder_name =  ''.join(random.choice(letters) for i in range(10))
        new_test_folder = os.path.join(root_dir, new_folder_name)
        shutil.move(test_folder, new_test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertIsNotNone(fake_handler.moved, "Observer did not detect folder move")
        self.assertTupleEqual((str(path), str(new_folder_name)), (str(fake_handler.moved[0]), str(fake_handler.moved[1])), "Observer did not detect folder move")

    def test_move_file(self):
        path = self.test_create_file()
        test_file = os.path.join(root_dir, path)
        # move file
        new_file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        new_path = pathlib.Path(new_file_name)
        new_test_file = os.path.join(root_dir, new_path)
        shutil.move(test_file, new_test_file)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertIsNotNone(fake_handler.moved, "Observer did not detect file move")
        self.assertTupleEqual((path, new_path), (fake_handler.moved[0], fake_handler.moved[1]), "Observer did not detect file move")

    def delete_dir(self):
        path = self.test_create_dir()
        test_folder = os.path.join(root_dir, path)
        # delete folder
        shutil.rmtree(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(fake_handler.deleted), str(path), "Observer did not detect folder deletion")

    def delete_file(self):
        path = self.test_create_file()
        test_file = os.path.join(root_dir, path)
        # delete file
        os.remove(test_file)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(fake_handler.deleted), str(path), "Observer did not detect file deletion")

def run_tests():
    time.sleep(2*SLEEP_CONSTANT) # need to wait for client to set up
    unittest.main(exit=False)
    global test_completed
    test_completed = True

def run_observer(observer : Observer):
    while not test_completed:
        observer.watch()
        time.sleep(SLEEP_CONSTANT)

def run():
    print("\nRunning client tests, takes ~30 seconds \nProgress bar given below")
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    global fake_handler
    fake_handler = FakeHandler()
    observer = Observer(root_dir, fake_handler.on_modify, fake_handler.on_move, fake_handler.on_create, fake_handler.on_delete)
    t1 = threading.Thread(target=run_observer, args=(observer,))
    t1.start()
    # REVIEW maybe this doesn't need a need thread to spin up?
    threading.Thread(target=run_tests).start()
    t1.join()
    shutil.rmtree(root_dir)
    print("completed running client tests")

if __name__ == "__main__":
    run()