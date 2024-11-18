#!/usr/bin/python3
import unittest
from models.state import State


class TestState(unittest.TestCase):
    """Test case for the State class"""

    def test_instance(self):
        state = State()
        self.assertIsInstance(state, State)

    def test_default_name(self):
        state = State()
        self.assertEqual(state.name, "")

