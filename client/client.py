import os
import time
import pathlib
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
            print("listening")
            observer.watch()
            time.sleep(SLEEP_CONSTANT)
    except KeyboardInterrupt:
        print("ending client")
    
def main():

    # TODO make command line arg
    DATA_DIR = "listen/" # for testing
    root_path = pathlib.Path(DATA_DIR)

    dispatcher = Dispatcher('http://127.0.0.1:5000/') # send data to server
    scan(root_path, dispatcher)

if __name__ == "__main__":
    main()