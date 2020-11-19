from collection import QuoteCollection
import yaml
import tkinter as tk

class Application:
    def __init__(self, filepath="./data.yml"):
        self.__filepath = filepath
        yaml_file = open(filepath, "r")
        yaml_object = yaml.safe_load(yaml_file.read())
        self.deserialise(yaml_object)
        yaml_file.close()

        self.window = tk.Tk()
    
    def deserialise(self, yaml_object):
        self.name = yaml_object["name"]
        self.collections = [QuoteCollection(collection_data) for collection_data in yaml_object["collections"]]

    def serialise(self):
        return {
            "name": self.name,
            "collections": [collection.serialise() for collection in self.collections]
        }
    
    def run(self):
        self.window.mainloop()

app = Application()
app.run()
