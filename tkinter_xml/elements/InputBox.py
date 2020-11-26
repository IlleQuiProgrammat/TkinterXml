import tkinter as TK
from tkinter import StringVar
from tkinter_xml.element_list import register_element
from tkinter_xml.constants import *
from tkinter_xml.elements.BaseElement import *

class InputBox(BaseElement):

    def __init__(self, attributes, children, parent_page, immediate_update=True):
        self._background = "#FFFFFF"
        self._border_width = 0
        self._contentVar = TK.StringVar()
        self._width = 0
        self._text = ""
        self._font_size = 12
        self._font_family = "Segoe UI"
        self._foreground = "black"
        
        super().__init__(attributes, children, parent_page, immediate_update)
    
    #region Properties

    @property
    def content(self):
        return self._contentVar.get()
    
    @content.setter
    def content(self, value):
        self._contentVar.set(value)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = value
        if self.immediate_update:
            self.reload()

    @property
    def border_width(self):
        return self._border_width
    
    @border_width.setter
    def border_width(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._border_width = to_set
        if self.immediate_update:
            self.reload()

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._width = to_set
        if self.immediate_update:
            self.reload()    

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        to_set = value
        if not isinstance(value, str):
            to_set = str(value)
        self._text = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def font_size(self):
        return self._font_size
    
    @font_size.setter
    def font_size(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._font_size = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def font_family(self):
        return self._font_family
    
    @font_family.setter
    def font_family(self, value):
        self._font_family = value
        if self.immediate_update:
            self.reload()
    

    @property
    def foreground(self):
        return self._foreground
    
    @foreground.setter
    def foreground(self, value):
        self._foreground = value
        if self.immediate_update:
            self.reload()

    #endregion Properties

    def backing_element_generator(self, parent):
        self.element = TK.Entry(parent)
        self.reload()
        return self.element

    def reload(self):
        self.element.config(
                        background=self.background,
                        borderwidth=self.border_width,
                        width=self.width,
                        text=self.text,
                        foreground=self.foreground,
                        font=(self.font_family, self.font_size),
                        textvariable=self._contentVar
                    )

register_element("InputBox", InputBox)