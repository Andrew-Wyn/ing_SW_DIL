#!/usr/bin/env python3

import unittest
import sys
import json
import cv2

from os import path

scriptdir = path.dirname(path.realpath(__file__))
sys.path.insert(0, f"{scriptdir}/../src/")

from document_CNN import Detectron

with open(f"{scriptdir}/../src/model/config.json") as f:
    config = json.load(f)

config["weights"] = f"{scriptdir}/../src/{config['weights']}"
model = Detectron(config["weights"], config["classes"])

class TestSet(unittest.TestCase):
    def test_tesserino(self):
        """
        test tesserino recognition
        """

        with open(f"{scriptdir}/test_tesserino.jpg", "rb") as f:
            image = f.read()

        result = model.recognize(image)
        del result[0]["snapshot"] # non possiamo testare la validita di bytes rappresentante lo snapshot
        expected = [
            {
                "type": "Tesserino",
                "attributes": {
                    "Nome": ["Luca","Moroni"],
                    "Matricola": ["311279"]
                },
                "valid": True,
                "primaryKey": ["311279"]
            }
        ]

        self.assertEqual(result, expected)

    def test_patente(self):
        """
        test patente recognition
        """

        with open(f"{scriptdir}/test_patente.jpg", "rb") as f:
            image = f.read()

        result = model.recognize(image)
        del result[0]["snapshot"] # non possiamo testare la validita di bytes rappresentante lo snapshot
        expected = [
            {
                "type": "Patente",
                "attributes": {
                    "Numero": ["TR5160189G"]
                },
                "valid": True,
                "primaryKey": ["TR5160189G"]
            }
        ]
        self.assertEqual(result, expected)

    def test_bg(self):
        """
        test bg recognition
        """

        with open(f"{scriptdir}/test_background.jpg", "rb") as f:
            image = f.read()

        result = model.recognize(image)
        expected = []
        self.assertEqual(result, expected)

    def test_bytestream(self):
        """
        test bytestream that don't represent a png image
        """

        bytestream = b'this is not an image'

        with self.assertRaises(cv2.error):
            result = model.recognize(bytestream)


if __name__ == '__main__':
    unittest.main()
