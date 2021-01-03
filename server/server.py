import os
import sys
import flask
import logging
import pathlib
from dropboxService import DropBoxService

app = flask.Flask(__name__)
dropbox : DropBoxService = None

@app.route('/', methods=["POST"])
def update():
    return "", 200

@app.route('/create_directory', methods=["POST"])
def create_directory():
    logging.info("create directory request")
    try:
        data = flask.request.form.to_dict()['data']
    except:
        return "Bad request", 400
    dropbox.create_directory(data)
    return "", 200

@app.route('/create_file', methods=["POST"])
def create_file():
    logging.info("create file request")
    try:
        file_path = flask.request.form.to_dict()['path']
        data = flask.request.files['data']
    except:
        return "Bad request", 400
    dropbox.create_file(file_path, data)
    return "", 200

@app.route('/modify_file', methods=["POST"])
def modify_file():
    logging.info("modify file request")
    try:
        file_path = flask.request.form.to_dict()['path']
        data = flask.request.files['data']
    except:
        return "Bad request", 400
    dropbox.modify_file(file_path, data.read())
    return "", 200

@app.route('/delete_directory', methods=["POST"])
def delete_directory():
    logging.info("delete directory request")
    try:
        file_path = flask.request.form.to_dict()['path']
    except:
        return "Bad request", 400
    dropbox.delete_directory(file_path)
    return "", 200

@app.route('/delete_file', methods=["POST"])
def delete_file():
    logging.info("delete file request")
    try:
        file_path = flask.request.form.to_dict()['path']
    except:
        return "Bad request", 400
    dropbox.delete_file(file_path)
    return "", 200

@app.route('/move', methods=["POST"])
def move_directory():
    logging.info("move request")
    try:
        dir_from = flask.request.form.to_dict()['from']
        dir_to = flask.request.form.to_dict()['to']
    except:
        return "Bad request", 400
    dropbox.move(dir_from, dir_to)
    return "", 200

def main():
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S %p')
    logging.info("starting server")
    if len(sys.argv) < 2:
        print("Need to provide path to folder to store files")
        logging.error("tried to start server without directory argument")
        exit()
    data_dir = pathlib.Path(sys.argv[1])
    if not os.path.exists(data_dir):
        print("Provided folder does not exist!")
        logging.error("tried to start server with invalid directory argument")
        exit()
    global dropbox
    dropbox = DropBoxService(data_dir)
    app.run(port=5000, host='0.0.0.0')

if __name__ == "__main__":
    main()