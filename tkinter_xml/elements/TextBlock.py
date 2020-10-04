import tkinter as TK
from tkinter_xml.elements.BaseElement import *

class TextBlock(BaseElement):
    default_attributes = {
        "Text": "",
        "FontSize": 12,
        "FontFamily": "Segoe UI",
        "Foreground": "black"
    }
    
    def backing_element_generator(self, parent):
        return TK.Label(parent,
                                text=self.default_attributes["Text"],
                                font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                foreground=self.default_attributes["Foreground"]
                        )