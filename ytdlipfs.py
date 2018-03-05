#!/bin/env python3
try:
    import ipfsapi
except ImportError:
    print("You need an ipfsapi module to run this program!")
    print("pip install ipfsapi")
    raise SystemExit
try:
    from ipfs_db import IPFSDB
except ImportError:
    print("You need an ipfs_db module to run this program!")
    print("pip install --user git+https://github.com/Efdecjanie/ipfs-db.git")
    raise SystemExit
try:
    import youtube_dl
except ImportError:
    print("You need youtube_dl!")
    raise SystemExit
try:
    from flask import Flask, request, send_from_directory
except ImportError:
    print("You need Flask!")
    raise SystemExit

import os
import json

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

ipfs = ipfsapi.connect()
db = IPFSDB()
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory("static/", "index.html")

@app.route('/add')
def add():
    url = request.values.get('url')
    if len(url) == 0:
        return "URL cannot be empty"
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s', 'logger': MyLogger()})

    with ydl:
        result = ydl.extract_info(
            url,
            download=True
        ) 
    dir = os.listdir()
    for name in dir:
        if name.split('.')[0] == result['id']:
            hash = db.add_file(str(name))
            os.remove(str(name))
            return hash

@app.route('/files.json')
def files_json():
    files = db.list_all_files()
    return json.dumps(files)
app.run(port=3600)
