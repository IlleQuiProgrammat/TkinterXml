import tkinter as TK
from tkinter_xml.constants import *
from tkinter_xml.elements.BaseElement import *

class Button(BaseElement):

    def __init__(self, attributes, children, parent_page, immediate_update=True):
        self._content = "Button"
        self._font_size = 12
        self._font_family = "Segoe UI"
        self._foreground = "black"
        self._click = lambda s: print("Button clicked")
        
        super().__init__(attributes, children, parent_page, immediate_update)
    
    #region Properties
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        self._content = value
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
    

    @property
    def click(self):
        return self._click
    
    @click.setter
    def click(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = getattr(self.parent_page, value)
        self._click = to_set
        if self.immediate_update:
            self.reload()
    #endregion Properties

    def backing_element_generator(self, parent):
        self.element = TK.Button(parent)
        self.reload()
        return self.element

    def reload(self):
        self.element.config(
                        text=self.content,
                        font=(self.font_family, self.font_size),
                        foreground=self.foreground,
                        command=lambda: (self.click)(self)
                    )
