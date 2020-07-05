import unittest

from src.document_CNN import Detectron

import json

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

        result = None
        self.assertIsNone(result)

    def test_patente(self):
        """
        test patente recognition
        """
        # data = {}

        result = None
        self.assertIsNone(result)
    
    def test_bg(self):
        """
        test bg recognition
        """
        # data = {}

        result = None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()