#!/usr/bin/python3
"""Unit tests for BaseModel class."""

import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def setUp(self):
        """Set up for each test."""
        self.model = BaseModel()

    def test_instance_creation(self):
        """Test if a new instance of BaseModel is created correctly."""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_id_unique(self):
        """Test that each BaseModel instance has a unique id."""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)

    def test_save_method(self):
        """Test if the save method updates 'updated_at'."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test if the to_dict method returns a correct dictionary."""
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(model_dict["created_at"], self.model.created_at.isoformat())
        self.assertEqual(model_dict["updated_at"], self.model.updated_at.isoformat())

    def test_from_dict(self):
        """Test creation of instance from dictionary."""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.model.id)
        self.assertEqual(new_model.created_at, self.model.created_at)
        self.assertEqual(new_model.updated_at, self.model.updated_at)


if __name__ == "__main__":
    unittest.main()
