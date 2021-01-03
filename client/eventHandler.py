import os
import logging
import pathlib
from dispatcher import Dispatcher

# Class to handel file system change events
class EventHandler:
    
    # init with the root path and the object to dispatch information to server
    def __init__(self, root_path : pathlib.Path, dispatcher : Dispatcher) -> None:
        self.root_path = root_path
        self.dispatcher = dispatcher

    def on_modify(self, path: pathlib.Path):
        file_path = os.path.join(self.root_path, path)
        try:
            with open(file_path, 'rb') as f:
                self.dispatcher.modify_file(path, f)
        except FileNotFoundError:
            logging.error("File lost during read for modification")
        logging.info("modified " + str(path))

    def on_move(self, path_from : pathlib.Path, path_to : pathlib.Path):
        self.dispatcher.move(str(path_from), str(path_to))
        logging.info("moved " + str(path_from) + " to " + str(path_to))

    def on_create(self, path : pathlib.Path, directory : bool):
        if (directory):
            self.dispatcher.create_directory(str(path))
        else:
            file_path = os.path.join(self.root_path, path)
            try:
                with open(file_path, 'rb') as f:
                    self.dispatcher.create_file(path, f)
            except FileNotFoundError:
                logging.error("File lost during read for modification")
        logging.info("new " +  str(path))

    def on_delete(self, path : pathlib.Path, directory : bool):
        self.dispatcher.delete(path, directory)
        logging.info("deleted " + str(path))