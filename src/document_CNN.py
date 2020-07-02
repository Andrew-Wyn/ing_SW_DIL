import os
import sys
import json
import datetime
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf

from mrcnn.config import Config
from mrcnn import model as modellib, utils


class InferenceConfig(Config):
    """Configuration for training on the toy  dataset.
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


class Detectron:
    def __init__(self, model_path):
        config = InferenceConfig()
        config.display()

        self._classes = ['BG', 'tesserino']
        self._model = modellib.MaskRCNN(mode="inference", config=config,  model_dir="./")
        self._model.load_weights(model_path, by_name=True)
        self._graph = tf.get_default_graph()

    def recognize(self, image):
        # Run object detection

        image = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        with self._graph.as_default():
            results = self._model.detect([image], verbose=1)

        # Display results
        r = results[0]

        ret = []

        for roi, class_id in zip(r["rois"], r["class_ids"]):
            y1, x1, y2, x2 = roi
            snapshot = image[y1:y2+1,x1:x2+1,:]
            # snapshot = image[x1:x2+1,y1:y2+1,:]
            snapshot = cv2.cvtColor(snapshot, cv2.COLOR_RGB2BGR)
            _, snapshot = cv2.imencode(".png", snapshot)

            cur_ret = {
                "type": str(class_id),
                "snapshot": snapshot.tobytes(),
                "attributes": {
                }
            }

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
    d = Detectron("mask_rcnn_.1593504868.7108881.h5")
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
