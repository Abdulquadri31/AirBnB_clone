import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.user import User
import json

class TestConsole(unittest.TestCase):
    """Test cases for the console"""

    def setUp(self):
        """Setup test environment"""
        self.cli = HBNBCommand()

    def tearDown(self):
        """Clean up storage after each test"""
        storage.all().clear()

    def test_create_instance(self):
        """Test creating a new instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            instance_id = f.getvalue().strip()
            self.assertIn("User.{}".format(instance_id), storage.all())

    def test_show_instance(self):
        """Test showing an instance based on its ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            instance_id = f.getvalue().strip()
            command = "show User {}".format(instance_id)
            with patch('sys.stdout', new=StringIO()) as f2:
                self.cli.onecmd(command)
                output = f2.getvalue().strip()
                self.assertIn(instance_id, output)

    def test_show_instance_not_found(self):
        """Test showing a non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show User non_existent_id")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_destroy_instance(self):
        """Test destroying an instance based on its ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            instance_id = f.getvalue().strip()
            command = "destroy User {}".format(instance_id)
            self.cli.onecmd(command)
            self.assertNotIn("User.{}".format(instance_id), storage.all())

    def test_destroy_instance_not_found(self):
        """Test destroying a non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy User non_existent_id")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_all_instances(self):
        """Test retrieving all instances of a class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            self.cli.onecmd("create User")
            self.cli.onecmd("User.all()")
            output = f.getvalue().strip().splitlines()
            self.assertEqual(len(output), 3)  # including two IDs and command output

    def test_count_instances(self):
        """Test counting all instances of a class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            self.cli.onecmd("create User")
            self.cli.onecmd("User.count()")
            output = f.getvalue().strip().splitlines()
            self.assertEqual(int(output[-1]), 2)  # Output should be count of 2

    def test_update_instance(self):
        """Test updating an instance with attribute name and value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            instance_id = f.getvalue().strip()
            command = 'update User {} first_name "John"'.format(instance_id)
            self.cli.onecmd(command)
            self.assertEqual(storage.all()["User.{}".format(instance_id)].first_name, "John")

    def test_update_instance_not_found(self):
        """Test updating a non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd('update User non_existent_id first_name "John"')
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_update_instance_dict(self):
        """Test updating an instance with a dictionary of attributes"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create User")
            instance_id = f.getvalue().strip()
            command = 'User.update({}, {{"first_name": "John", "age": 30}})'.format(instance_id)
            self.cli.onecmd(command)
            instance = storage.all()["User.{}".format(instance_id)]
            self.assertEqual(instance.first_name, "John")
            self.assertEqual(instance.age, 30)

    def test_show_help(self):
        """Test help message for the 'show' command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("help show")
            output = f.getvalue().strip()
            self.assertIn("Retrieve an instance based on its ID", output)

    def test_update_help(self):
        """Test help message for the 'update' command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("help update")
            output = f.getvalue().strip()
            self.assertIn("Updates an instance based on its ID", output)

    def test_unknown_command(self):
        """Test unknown command handling"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("unknowncommand")
            self.assertEqual(f.getvalue().strip(), "*** Unknown syntax: unknowncommand")


if __name__ == "__main__":
    unittest.main()
