import tkinter as TK
from tkinter_xml.elements.BaseElement import *

class TextBlock(BaseElement):

    def __init__(self, attributes, children, parent_page):
        self.default_attributes = {
            "Text": "",
            "FontSize": 12,
            "FontFamily": "Segoe UI",
            "Foreground": "black"
        }
        
        super().__init__(attributes, children, parent_page)
    
    def backing_element_generator(self, parent):
        return TK.Label(parent,
                                text=self.default_attributes["Text"],
                                font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                foreground=self.default_attributes["Foreground"]
                        )