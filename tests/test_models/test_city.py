#!/usr/bin/python3
import unittest
from models.city import City


class TestCity(unittest.TestCase):
    """Test case for the City class"""

    def test_instance(self):
        city = City()
        self.assertIsInstance(city, City)

    def test_default_state_id(self):
        city = City()
        self.assertEqual(city.state_id, "")

    def test_default_name(self):
        city = City()
        self.assertEqual(city.name, "")
