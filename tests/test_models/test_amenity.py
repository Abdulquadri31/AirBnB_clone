#!/usr/bin/python3
import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test case for the Amenity class"""

    def test_instance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)

    def test_default_name(self):
        amenity = Amenity()
        self.assertEqual(amenity.name, "")
