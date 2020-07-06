import unittest

from src.document_CNN import Detectron

import json
import cv2

class TestSet(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSet, self).__init__(*args, **kwargs)
        
        with open("test/config.json") as f:
            config = json.load(f)

        self._model = Detectron(config["weights"], config["classes"])

    def test_tesserino(self):
        """
        test tesserino recognition
        """
        # data = {}

        with open("test/test_tesserino.jpg", "rb") as f:
            image = f.read()


        result = self._model.recognize(image)
        attributes = result[0]["attributes"]
        expected = json.loads('{"Matricola": ["311279"], "Nome": ["Luca", "Moroni"]}')
        self.assertEqual(attributes, expected)

    def test_patente(self):
        """
        test patente recognition
        """
        # data = {}

        with open("test/test_backgroud.jpg", "rb") as f:
            image = f.read()

        result = self._model.recognize(image)

        expected = []

        self.assertEqual(result, expected)
    
    def test_bg(self):
        """
        test bg recognition
        """
        # data = {}

        result = None
        self.assertIsNone(result)
    
    def test_bytestream(self):
        """
        test bytestream that don't represent a png image
        """

        bytestream = b'nasdasd'

        with self.assertRaises(cv2.error):
            result = self._model.recognize(bytestream)


if __name__ == '__main__':
    unittest.main()