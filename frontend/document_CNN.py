import os
import sys
import json
import datetime
import numpy as np
import cv2
# from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt

# # Root directory of the project
# ROOT_DIR = os.path.abspath("./")

# # Import Mask RCNN
# sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# # Path to trained weights file
# COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# # Directory to save logs and model checkpoints, if not provided
# # through the command line argument --logs
# DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

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
        self._classes = ['BG', 'tesserino']

        config = InferenceConfig()
        config.display()

        self._model = modellib.MaskRCNN(mode="inference", config=config,  model_dir="./")
        self._model.load_weights(model_path, by_name=True)

    def recognize(self, image):
        # Run object detection

        image = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self._model.detect([image], verbose=1)
        # Display results
        r = results[0]

        return r["rois"]

        # /Users/lucamoroni/Downloads/tesserino21.jpg
        

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
    d = Detectron("mask_rcnn_.1593520466.6446981.h5")
    with open("/Users/lucamoroni/Downloads/tesserino21.jpg", "rb") as f:
        bs = f.read()
    rois = d.recognize(bs)
    breakpoint()
    print()
