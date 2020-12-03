from quote_lib.collection import QuoteCollection
import yaml
import tkinter as tk

class ApplicationRepresentation:
    def __init__(self, filepath="./data.yml"):
        self.__filepath = filepath
        yaml_file = open(filepath, "r")
        yaml_object = yaml.safe_load(yaml_file.read())
        self.deserialise(yaml_object)
        yaml_file.close()
    
    def deserialise(self, yaml_object):
        self.name = yaml_object["name"]
        self.collections = [QuoteCollection(collection_data) for collection_data in yaml_object["collections"]]

    def serialise(self):
        return {
            "name": self.name,
            "collections": [collection.serialise() for collection in self.collections]
        }

    def save(self):
        ser = self.serialise()
        yaml_file = open(self.__filepath, 'w')
        yaml_file.write(yaml.dump(ser))
        yaml_file.close()