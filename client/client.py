import os
import sys
import time
import pathlib
import logging
from observer import Observer
from dispatcher import Dispatcher
from eventHandler import EventHandler

SLEEP_CONSTANT = 2.5

''' 
    Function listens to run the observer on a while loop
'''
def scan(root_path : pathlib.Path, dispatcher : Dispatcher):
    handler = EventHandler(root_path, dispatcher) # converts changes to information which is dispatched to server
    # Observer watchs for change has functions to call in the event of change
    observer = Observer(root_path, handler.on_modify, handler.on_move, 
                        handler.on_create, handler.on_delete) 
    try:
        while True:
            observer.watch()
            time.sleep(SLEEP_CONSTANT)
    except KeyboardInterrupt:
        logging.info("client shutdown")
    
def main():
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.info("Logger started")
    if len(sys.argv) < 2:
        print("Need to provide path to folder to listen to")
        logging.error("attempt to start client without folder")
        exit()
    root_dir = pathlib.Path(sys.argv[1])
    if not os.path.exists(root_dir):
        print("Provided folder does not exist!")
        logging.error("attempt to input invalid listening directory")
        exit()
    root_path = pathlib.Path(root_dir)
    if len(sys.argv) >= 3:
        dispatcher = Dispatcher(sys.argv[2])
    else:
        dispatcher = Dispatcher('http://127.0.0.1:5000/') # send data to server
    scan(root_path, dispatcher)

if __name__ == "__main__":
    main()