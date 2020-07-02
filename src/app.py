#!/bin/env python3

from flask import Flask, request, render_template
from base64 import b64decode, b64encode
import json

from document_CNN import Detectron


app = Flask(__name__)

with open("config.json") as f:
    config = json.load(f)

detectron = Detectron(config["weights"], config["classes"])


@app.route('/recognize', methods=["POST"])
def recognize():
    image = b64decode(request.json["image"]) # bytes object (representing the image)
    data = detectron.recognize(image) # returns a list of dicts dict
    for entry in data:
        entry["snapshot"] = b64encode(entry["snapshot"]).decode()
    return json.dumps(data)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', ssl_context='adhoc')
