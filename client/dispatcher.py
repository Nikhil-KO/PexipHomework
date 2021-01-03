import requests
import logging

# Class sends the information from the handler to server
class Dispatcher:

    def __init__(self, url : str) -> None:
        self.url = url

    def create_directory(self, path : str):
        data =  {'data': path}
        x = requests.post(self.url + 'create_directory', data=data)
        logging.info(x)
    
    def create_file(self, path : str, data):
        info  = {'path': path}
        files = {'data': data}
        x = requests.post(self.url + 'create_file', data=info, files=files)
        logging.info(x)
    
    def modify_file(self, path : str, data):
        info  = {'path': path}
        files = {'data': data}
        x = requests.post(self.url + 'modify_file', data=info, files=files)
        logging.info(x)

    def delete(self, path : str, directory : bool):
        data = {'path': path}
        if directory:
            x = requests.post(self.url + 'delete_directory', data=data)
        else:
            x = requests.post(self.url + 'delete_file', data=data)
        logging.info(x)
    
    def move(self, path_from : str, path_to : str):
        data = {
            'from': path_from,
            'to': path_to
            }
        x = requests.post(self.url + 'move', data=data)
        logging.info(x)