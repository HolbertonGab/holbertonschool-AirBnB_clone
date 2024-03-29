#!/usr/bin/env python3
"""
Console that contains the entry point of the command interpreter.
"""

import cmd
from models.base_model import BaseModel
from models import storage
import json
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    This class defines console functions
    """

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")
        return True

    def emptyline(self):
        """Handles empty line"""
        pass

    def do_create(self, arg):
        """Create an instanciate, save it, and print ID"""
        if not arg:
            print("** class name missing **")
            return

        class_name = arg.split()[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        new_instance = globals()[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """A string representation of class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance and save it in Json file"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        if not arg:
            for instance in storage.all().values():
                print(instance)
            return

        class_name = arg.split()[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        all_instances = []
        for key, instance in storage.all().items():
            if key.split('.')[0] == class_name:
                all_instances.append(str(instance))

        if not all_instances:
            print("** no instances found **")
        else:
            print('\n'.join(all_instances))

    def do_update(self, arg):
        """Update instance from class name and id, or updating attributes"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all():
            print("** no instance found **")
            return

        instance = storage.all()[key]

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return

        attribute_value_str = args[3]

        if not (attribute_value_str.isdigit() or '.' in attribute_value_str):
            try:
                attribute_value = float(attribute_value_str)
            except ValueError:
                attribute_value = attribute_value_str

        else:
            attribute_value = type(getattr(instance, attribute_name))
            (attribute_value_str)

        if attribute_name in ["id", "created_at", "updated_at"]:
            print("** cannot update id, created_at, or updated_at **")
            return

        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
