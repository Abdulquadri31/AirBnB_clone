#!/usr/bin/python3
"""This module defines the HBNBCommand class, a command interpreter for the AirBnB clone."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone project."""
    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "City": City,
        "State": State,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Override default behavior to do nothing on empty input"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class, save it, and print its id"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        instance = self.classes[arg]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Show the string representation of an instance based on class and ID"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on class and ID, and save changes"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Print all instances or all instances of a specific class"""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        objs = [
            str(obj)
            for key, obj in storage.all().items()
            if not arg or key.startswith(arg)
        ]
        print(objs)

    def do_update(self, arg):
        """Update an instance based on class name and ID by adding or updating attributes"""
        args = arg.split(" ", 2)
        if len(args) == 0 or not args[0]:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1 or not args[1]:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return

        instance = storage.all()[key]
        # Check if third argument is a dictionary
        if args[2].startswith("{") and args[2].endswith("}"):
            # Evaluate the dictionary string into a Python dictionary
            try:
                updates = eval(args[2])
                if isinstance(updates, dict):
                    for attr, value in updates.items():
                        setattr(instance, attr, value)
                    instance.save()
            except Exception as e:
                print(f"** error processing dictionary: {e} **")
            return

        # Process as attribute-value pair
        attr_and_value = args[2].split(" ", 1)
        if len(attr_and_value) < 2:
            print("** value missing **")
            return
        attr_name = attr_and_value[0]
        attr_value = attr_and_value[1].strip('"\'')  # Remove quotes if any

        # Attempt to convert to appropriate type
        try:
            if attr_value.isdigit():
                attr_value = int(attr_value)
            elif attr_value.replace('.', '', 1).isdigit() and attr_value.count('.') == 1:
                attr_value = float(attr_value)
        except ValueError:
            pass

        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_count(self, arg):
        """Count the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all() if key.startswith(arg))
        print(count)

    def default(self, line):
        """Handle <class name>.<command>(<args>) syntax"""
        parts = line.split(".", 1)
        if len(parts) == 2 and parts[0] in self.classes:
            class_name = parts[0]
            cmd_and_args = parts[1]
            if cmd_and_args.startswith("all()"):
                self.do_all(class_name)
            elif cmd_and_args.startswith("count()"):
                self.do_count(class_name)
            elif cmd_and_args.startswith("show("):
                instance_id = cmd_and_args[5:-1].strip('"\'')
                self.do_show(f"{class_name} {instance_id}")
            elif cmd_and_args.startswith("destroy("):
                instance_id = cmd_and_args[8:-1].strip('"\'')
                self.do_destroy(f"{class_name} {instance_id}")
            elif cmd_and_args.startswith("update("):
                args = cmd_and_args[7:-1]
                if "{" in args and "}" in args:
                    instance_id, dict_repr = args.split(", ", 1)
                    instance_id = instance_id.strip('"\'')
                    self.do_update(f"{class_name} {instance_id} {dict_repr}")
                else:
                    args = args.split(", ", 2)
                    if len(args) == 3:
                        instance_id = args[0].strip('"\'')
                        attr_name = args[1].strip('"\'')
                        attr_value = args[2].strip('"\'')
                        self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
