#!/usr/bin/python3
"""This module defines the class (FileStorage)"""
from json import dump, load
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class is used to serialized and deserializated an object
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionnary (__objects)."""
        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id"""
        name = obj.__class__.__name__
        key = "{}.{}".format(name, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Save all objects contains in (__objetcs) to a file."""
        buff__obj = FileStorage.__objects
        __obj_to_dict = {}
        for (key, dic) in buff__obj.items():
            __obj_to_dict[key] = dic.to_dict()
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as file:
            dump(__obj_to_dict, file)

    def reload(self):
        """Recreate each object storage in the JSON file, if it exist"""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r', encoding="utf-8") as file:
                obj = load(file)
                for (key, value) in obj.items():
                    _class_name = globals()[value['__class__']]
                    instance = _class_name(**value)
                    FileStorage.__objects[key] = instance
