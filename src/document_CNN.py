import os
import sys
import json
import datetime
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import re

from mrcnn.config import Config
from mrcnn import model as modellib, utils
from pytesseract import image_to_data, Output
from collections import namedtuple


OcrRecord = namedtuple("OcrRecord", "conf,text,x,y,w,h")


class InferenceConfig(Config):
    """
    Configuration for training on the toy dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "document"

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + tesserino // scalare

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 41

    LEARNING_RATE=0.006

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


# classes = {
#     "tesserino": {
#     "lang": "ita",
#     "min_conf": 80,
#     "regions": [
#       {
#         "nome": "Matricola",
#         "type": "box"/"regex",
#         "rule": [x1, y1, x2, y2] / "testo della regex",
#         "needed": True/False
#       }, {
#         # altra region
#       }
#     ]
#   }
# }


def check_box(snap_w, snap_h, ocr_x1, ocr_y1, ocr_w, ocr_h, x1, y1, x2, y2):
    x1 = int(snap_w*x1)
    x2 = int(snap_w*x2)
    y1 = int(snap_h*y1)
    y2 = int(snap_h*y2)

    ocr_x2 = ocr_x1 + ocr_w - 1
    ocr_y2 = ocr_y1 + ocr_h - 1

    return x1 <= ocr_x1 and ocr_x2 <= x2 and y1 <= ocr_y1 and ocr_y2 <= y2


class Detectron:
    def __init__(self, weights_path, classes):
        config = InferenceConfig()
        config.display()

        self._classes = classes
        self._class_names = list(self._classes)
        self._model = modellib.MaskRCNN(mode="inference", config=config,  model_dir="./")
        self._model.load_weights(weights_path, by_name=True)
        # self._graph = tf.get_default_graph()

        self._model.keras_model._make_predict_function()

        for class_ in classes.values():
            for region in class_["regions"]:
                if region["type"] == "regex":
                    region["rule"] = re.compile(region["rule"], re.IGNORECASE)

    def recognize(self, image):
        image = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #with self._graph.as_default():
        results = self._model.detect([image], verbose=1)

        # Display results
        r = results[0]

        ret = []

        for roi, class_id in zip(r["rois"], r["class_ids"]):
            class_name = self._class_names[class_id-1]
            y1, x1, y2, x2 = roi
            snapshot = image[y1:y2+1,x1:x2+1,:]
            snapshot_h, snapshot_w, _ = snapshot.shape
            ocr_data = image_to_data(snapshot, lang=self._classes[class_name]["lang"], output_type=Output.DICT)

            ocr_data["conf"] = [int(c) for c in ocr_data["conf"]]
            ocr_data = [OcrRecord(*t) for t in zip(ocr_data["conf"], ocr_data["text"], ocr_data["top"], ocr_data["left"], ocr_data["width"], ocr_data["height"])]
            ocr_data = [ocr for ocr in ocr_data if ocr.conf >= self._classes[class_name]["min_conf"] and ocr.text.strip()]

            snapshot = cv2.cvtColor(snapshot, cv2.COLOR_RGB2BGR)
            _, snapshot = cv2.imencode(".png", snapshot)

            cur_ret = {
                "type": class_name,
                "snapshot": snapshot.tobytes(),
                "attributes": {}
            }

            found = set()

            for ocr in ocr_data:
                for region in self._classes[class_name]["regions"]:
                    name = region["name"]
                    rule = region["rule"]

                    if name in found:
                        continue

                    if region["type"] == "box":
                        if check_box(snapshot_w, snapshot_h, ocr.x, ocr.y, ocr.w, ocr.h, *rule):
                            break
                    elif region["type"] == "regex":
                        if rule.search(ocr.text):
                            break
                else:
                    continue

                cur_ret["attributes"][name] = ocr.text
                found.add(name)

            ret.append(cur_ret)

        return ret


def recognize_dummy(image):
    return [{
       "type": "Carta d'Identità",
        "snapshot": image,
        "attributes": {
            "name": "",
            "id": ""
        }
    }]


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)
    d = Detectron(config["weights"], config["classes"])
    with open("test1.jpg", "rb") as f:
        bs = f.read()
    rets = d.recognize(bs)
    print()
    if len(rets) == 0:
        print("Nothing found")
    else:
        print("Found something")
        with open("output.png", "wb") as f:
            f.write(rets[0]["snapshot"])
