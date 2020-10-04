import tkinter as TK
from tkinter_xml.constants import *
from tkinter_xml.elements.BaseElement import *

class Button(BaseElement):
    default_attributes = {
        "Content": "Button",
        "FontSize": 12,
        "FontFamily": "Segoe UI",
        "Foreground": "black",
        "Click": lambda s: print("Button clicked"),
    }
    custom_attributes = {}
    def __init__(self, attributes, children):
        for attribute in attributes.keys():
            if '.' in attribute:
                custom_attribute_prefix = attribute.split('.')[0]
                if custom_attribute_prefix in self.custom_attributes:
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                else:
                    self.custom_attributes[custom_attribute_prefix] = {}
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                continue
            if attribute not in self.default_attributes:
                raise Exception(f"Encountered an invalid attribute on Button: {attribute}")
            else:
                if attribute in EVENT_HANDLERS:
                    self.default_attributes[attribute] = eval(attributes[attribute])
                else:
                    self.default_attributes[attribute] = attributes[attribute]
                
        self.backing_element_generator = self.generate_backing_element()
    
    def generate_backing_element(self):
        return lambda parent: TK.Button(parent,
                                        text=self.default_attributes["Content"],
                                        font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                        foreground=self.default_attributes["Foreground"],
                                        command=lambda: self.default_attributes["Click"](self)
                                )
