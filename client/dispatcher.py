import requests

class Dispatcher:

    def __init__(self, url : str) -> None:
        self.url = url

    def create_directory(self, path : str):
        data =  {'data': path}
        x = requests.post(self.url + 'create_directory', data=data)
        print(x)
    
    def create_file(self, path : str, data):
        info  = {'path': path}
        files = {'data': data}
        x = requests.post(self.url + 'create_file', data=info, files=files)
        print(x)