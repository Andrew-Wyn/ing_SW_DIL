#!/usr/bin/env python3
import unittest
import sys
import json
import cv2

from os import path

scriptdir = path.dirname(path.realpath(__file__))
sys.path.insert(0, f"{scriptdir}/../src/")

from document_CNN import Detectron

class TestSet(unittest.TestCase):
    def __init__(self, *args, **kwargs):
            try:
                _ = self._model
            except AttributeError:
                super().__init__(*args, **kwargs)

                with open(f"{scriptdir}/../src/model/config.json") as f:
                    config = json.load(f)

                config["weights"] = f"{scriptdir}/../src/{config['weights']}"
                self._model = Detectron(config["weights"], config["classes"])

    def test_tesserino(self):
        """
        test tesserino recognition
        """

        with open(f"{scriptdir}/../test/test_tesserino.jpg", "rb") as f:
            image = f.read()

        result = self._model.recognize(image)

        del result[0]["snapshot"] # non possiamo testare la validita di bytes rappresentante lo snapshot

        expected = json.loads('[{"type": "Tesserino","attributes": {"Nome": ["Luca","Moroni"],"Matricola": ["311279"]},"valid": true,"primaryKey": ["311279"]}]')
        self.assertEqual(result, expected)

    def test_patente(self):
        """
        test patente recognition
        """

        with open(f"{scriptdir}/../test/test_patente.jpg", "rb") as f:
            image = f.read()

        result = self._model.recognize(image)

        del result[0]["snapshot"] # non possiamo testare la validita di bytes rappresentante lo snapshot

        expected = json.loads('[{"type": "Patente","attributes": {"Numero": ["TR5160189G"]},"valid": true,"primaryKey": ["TR5160189G"]}]')
        self.assertEqual(result, expected)

    def test_bg(self):
        """
        test bg recognition
        """

        with open(f"{scriptdir}/../test/test_backgroud.jpg", "rb") as f:
            image = f.read()

        result = self._model.recognize(image)

        expected = []

        self.assertEqual(result, expected)

    def test_bytestream(self):
        """
        test bytestream that don't represent a png image
        """

        bytestream = b'nasdasd'

        with self.assertRaises(cv2.error):
            result = self._model.recognize(bytestream)


if __name__ == '__main__':
    unittest.main()
