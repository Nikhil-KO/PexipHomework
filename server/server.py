import os
import sys
import pathlib
import flask
from dropboxService import DropBoxService

app = flask.Flask(__name__)
dropbox : DropBoxService = None
DATA_DIR = pathlib.Path("server_data/")

@app.route('/', methods=["POST"])
def update():
    return "", 200

@app.route('/create_directory', methods=["POST"])
def create_directory():
    try:
        data = flask.request.form.to_dict()['data']
    except:
        return "Bad request", 400
    print(data)
    dropbox.create_directory(data)
    return "", 200

@app.route('/create_file', methods=["POST"])
def create_file():
    try:
        file_path = flask.request.form.to_dict()['path']
        data = flask.request.files['data']
    except:
        return "Bad request", 400
    dropbox.create_file(file_path, data)
    return "", 200

@app.route('/modify_file', methods=["POST"])
def modify_file():
    try:
        file_path = flask.request.form.to_dict()['path']
        data = flask.request.files['data']
    except:
        return "Bad request", 400
    dropbox.modify_file(file_path, data.read())
    return "", 200

@app.route('/delete_directory', methods=["POST"])
def delete_directory():
    try:
        file_path = flask.request.form.to_dict()['path']
    except:
        return "Bad request", 400
    dropbox.delete_directory(file_path)
    return "", 200

@app.route('/delete_file', methods=["POST"])
def delete_file():
    try:
        file_path = flask.request.form.to_dict()['path']
    except:
        return "Bad request", 400
    dropbox.delete_file(file_path)
    return "", 200

@app.route('/move', methods=["POST"])
def move_directory():
    try:
        dir_from = flask.request.form.to_dict()['from']
        dir_to = flask.request.form.to_dict()['to']
    except:
        return "Bad request", 400
    dropbox.move(dir_from, dir_to)
    return "", 200

def main():
    print("starting server")
    global dropbox
    dropbox = DropBoxService(pathlib.Path("server_data/"))
    # if len(sys.argv) < 2:
    #     raise "Directory to listen on must be passed to script"
    #     exit
    # DATA_DIR = sys.argv[1]

    #print(DATA_DIR)

    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    main()