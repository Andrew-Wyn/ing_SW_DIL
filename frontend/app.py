#!/bin/env python3


from flask import Flask, request, render_template
from base64 import b64decode, b64encode
import json

import document_CNN

MODEL_PATH = ""

app = Flask(__name__)


@app.route('/recognize', methods=["POST"])
def recognize():
    image = b64decode(request.json["image"]) # bytes object (representing the image)
    data = document_CNN.recognize(image) # returns a list of dicts dict
    for entry in data:
        entry["snapshot"] = b64encode(entry["snapshot"]).decode()
    return json.dumps(data)


@app.route('/')
def index():
    return render_template("index.html")