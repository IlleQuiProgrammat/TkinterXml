import tkinter as TK
from tkinter_xml.constants import *
from tkinter_xml.elements.BaseElement import *

class Button(BaseElement):

    def __init__(self, attributes, children, parent_page):
        self.default_attributes = {
            "Content": "Button",
            "FontSize": 12,
            "FontFamily": "Segoe UI",
            "Foreground": "black",
            "Click": lambda s: print("Button clicked"),
        }
        
        super().__init__(attributes, children, parent_page)
    
    def backing_element_generator(self, parent):
        return TK.Button(parent,
                            text=self.default_attributes["Content"],
                            font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                            foreground=self.default_attributes["Foreground"],
                            command=lambda: self.default_attributes["Click"](self)
                    )
