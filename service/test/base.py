import sys
import os
import unittest
from fastapi.testclient import TestClient

# Adiciona o diretório 'service' ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import create_api


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Configura a app para o modo de teste
        self.app = create_api("testing")
        self.client = TestClient(self.app)
