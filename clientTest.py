import os
import time
import shutil
import string
import random
import pathlib
import unittest
import threading
from client.observer import Observer

test_completed = False
SLEEP_CONSTANT = 2
letters = string.ascii_lowercase

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

class ClientUnitTests(unittest.TestCase):
    
    def __init__(self, methodName: str, handle : FakeHandler, root_dir : pathlib.Path) -> None:
        super().__init__(methodName=methodName)
        self.handle = handle
        self.root_dir = root_dir

    def test_create_dir(self):
        folder_name = ''.join(random.choice(letters) for i in range(10))
        path = pathlib.Path(folder_name)
        test_folder = os.path.join(self.root_dir, path)
        os.makedirs(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up directory being made")

    def test_create_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        path = pathlib.Path(file_name)
        test_file = os.path.join(self.root_dir, path)
        with open(test_file, 'w') as f:
            print("unit test file", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up file being made")

    def test_modify_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        path = pathlib.Path(file_name)
        test_file = os.path.join(self.root_dir, path)
        with open(test_file, 'w') as f:
            print("unit test file", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up file being made")
        # modify contents
        with open(test_file, 'w') as f:
            print("modifed text", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.modified), str(path), "Observer did not pick up file being modified")

    def test_move_dir(self):
        folder_name = ''.join(random.choice(letters) for i in range(10))
        path = pathlib.Path(folder_name)
        test_folder = os.path.join(self.root_dir, path)
        os.makedirs(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up directory being made")
        new_folder_name =  ''.join(random.choice(letters) for i in range(10))
        new_test_folder = os.path.join(self.root_dir, new_folder_name)
        # move folder
        shutil.move(test_folder, new_test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertIsNotNone(self.handle.moved, "Observer did not detect folder move")
        self.assertTupleEqual((str(path), str(new_folder_name)), (str(self.handle.moved[0]), str(self.handle.moved[1])), "Observer did not detect folder move")

    def test_move_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        path = pathlib.Path(file_name)
        test_file = os.path.join(self.root_dir, path)
        with open(test_file, 'w') as f:
            print("unit test file", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up file being made")
        # move file
        new_file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        new_path = pathlib.Path(new_file_name)
        new_test_file = os.path.join(self.root_dir, new_path)
        shutil.move(test_file, new_test_file)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertIsNotNone(self.handle.moved, "Observer did not detect file move")
        self.assertTupleEqual((path, new_path), (self.handle.moved[0], self.handle.moved[1]), "Observer did not detect file move")

    def delete_dir(self):
        folder_name = ''.join(random.choice(letters) for i in range(10))
        path = pathlib.Path(folder_name)
        test_folder = os.path.join(self.root_dir, path)
        os.makedirs(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up directory being made")
        # delete folder
        shutil.rmtree(test_folder)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.deleted), str(folder_name), "Observer did not detect folder deletion")

    def delete_file(self):
        file_name = ''.join(random.choice(letters) for i in range(10)) + ".txt"
        path = pathlib.Path(file_name)
        test_file = os.path.join(self.root_dir, path)
        with open(test_file, 'w') as f:
            print("unit test file", file=f)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.created), str(path), "Observer did not pick up file being made")
        # delete file
        os.remove(test_file)
        time.sleep(2 * SLEEP_CONSTANT)
        self.assertEqual(str(self.handle.deleted), str(path), "Observer did not detect file deletion")

def run_tests(handle : FakeHandler, root_dir : pathlib.Path):
    print("running client tests")
    time.sleep(2*SLEEP_CONSTANT) # need to wait for client to set up
    test_suite = unittest.TestSuite()
    test_suite.addTest(ClientUnitTests('test_create_dir', handle, root_dir))
    test_suite.addTest(ClientUnitTests('test_create_file', handle, root_dir))
    test_suite.addTest(ClientUnitTests('test_modify_file', handle, root_dir))
    test_suite.addTest(ClientUnitTests('test_move_dir', handle, root_dir))
    test_suite.addTest(ClientUnitTests('test_move_file', handle, root_dir))
    test_suite.addTest(ClientUnitTests('delete_dir', handle, root_dir))
    test_suite.addTest(ClientUnitTests('delete_file', handle, root_dir))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
    global test_completed
    test_completed = True

def run_observer(observer : Observer):
    while not test_completed:
        observer.watch()
        time.sleep(SLEEP_CONSTANT)

def run():
    root_dir = pathlib.Path('client/listen')
    fake_handler = FakeHandler()
    observer = Observer(root_dir, fake_handler.on_modify, fake_handler.on_move, fake_handler.on_create, fake_handler.on_delete)
    t1 = threading.Thread(target=run_observer, args=(observer,))
    t1.start()
    # REVIEW maybe this doesn't need a need thread to spin up?
    threading.Thread(target=run_tests, args=(fake_handler, root_dir,)).start()
    t1.join()

if __name__ == "__main__":
    run()