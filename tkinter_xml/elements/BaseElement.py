import tkinter as TK
from tkinter_xml.constants import *
class BaseElement():
    default_attributes = {}
    custom_attributes = {}

    def __init__(self, attributes, children):
        self.children = children
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
    
    def backing_element_generator(self, parent):
        return TK.Frame()