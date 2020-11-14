import tkinter as TK
from tkinter_xml.constants import *

class BaseElement():
    def __init__(self, attributes, children, parent_page, immediate_update):
        self.custom_attributes = {}
        self.immediate_update = False
        self.children = children
        self.parent_page = parent_page
        for attribute in attributes.keys():
            if 'x_Name' == attribute:
                setattr(parent_page, attributes[attribute], self)
            elif '.' in attribute:
                custom_attribute_prefix = attribute.split('.')[0]
                if custom_attribute_prefix in self.custom_attributes:
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                else:
                    self.custom_attributes[custom_attribute_prefix] = {}
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
            elif not hasattr(self, attribute) or isinstance(getattr(self, attribute), property):
                raise Exception(f"Encountered an invalid attribute on element {self}: {attribute} on {dir(self)} ({type(getattr(self, attribute))})")
            else:
                setattr(self, attribute, attributes[attribute])
        self.immediate_update = immediate_update
    
    def backing_element_generator(self, parent):
        return TK.Frame()