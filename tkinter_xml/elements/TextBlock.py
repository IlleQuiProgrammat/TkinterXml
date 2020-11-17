import tkinter as TK
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.element_list import register_element

class TextBlock(BaseElement):

    def __init__(self, attributes, children, parent_page, immediate_update=True):        
        #region set_default_properties
        self._active_background = "white"
        self._active_foreground = "black"
        self._anchor = TK.CENTER
        self._background = "#E4E4E4"
        self._bitmap = ""
        self._border_width = 0
        self._compound = TK.NONE
        self._cursor = "arrow",
        self._disabled_foreground = "black"
        self._font_size = 12
        self._font_family = "Segoe UI"
        self._foreground = "black"
        self._height = 0
        self._highlight_background = "white"
        self._highlight_foreground = "black"
        self._highlight_thickness = 0
        self._image = ""
        self._justify = TK.CENTER
        self._padding = (1, 1)
        self._relief = TK.FLAT
        self._state = TK.NORMAL
        self._take_focus = False
        self._text = ""
        self._underline = -1
        self._width = 0
        self._wrap_length = 0
        #endregion set_default_properties

        super().__init__(attributes, children, parent_page, immediate_update)
    # TODO: Investigate if theres a way to set these in a loop preserving autocomplete
    #region properties
    @property
    def active_background(self):
        return self._active_background
    
    @active_background.setter
    def active_background(self, value):
        self._active_background = value
        if self.immediate_update:
            self.reload()
    

    @property
    def active_foreground(self):
        return self._active_foreground
    
    @active_foreground.setter
    def active_foreground(self, value):
        self._active_foreground = value
        if self.immediate_update:
            self.reload()
    

    @property
    def anchor(self):
        return self._anchor
    
    @anchor.setter
    def anchor(self, value):
        # TODO: Work out to use enum names or values, currently using values
        self._anchor = value
        if self.immediate_update:
            self.reload()
    

    @property
    def background(self):
        return self._background
    
    @background.setter
    def background(self, value):
        self._background = value
        if self.immediate_update:
            self.reload()
    

    @property
    def bitmap(self):
        return self._bitmap
    
    @bitmap.setter
    def bitmap(self, value):
        # FIXME: Not sure what type this is, leaving as string for now
        self._bitmap = value
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
    def compound(self):
        return self._compound
    
    @compound.setter
    def compound(self, value):
        self._compound = value
        if self.immediate_update:
            self.reload()
    

    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, value):
        self._cursor = value
        if self.immediate_update:
            self.reload()
    

    @property
    def disabled_foreground(self):
        return self._disabled_foreground
    
    @disabled_foreground.setter
    def disabled_foreground(self, value):
        self._disabled_foreground = value
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
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._height = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def highlight_background(self):
        return self._highlight_background
    
    @highlight_background.setter
    def highlight_background(self, value):
        self._highlight_background = value
        if self.immediate_update:
            self.reload()
    

    @property
    def highlight_foreground(self):
        return self._highlight_foreground
    
    @highlight_foreground.setter
    def highlight_foreground(self, value):
        self._highlight_foreground = value
        if self.immediate_update:
            self.reload()
    

    @property
    def highlight_thickness(self):
        return self._highlight_thickness
    
    @highlight_thickness.setter
    def highlight_thickness(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._highlight_thickness = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, value):
        self._image = value
        if self.immediate_update:
            self.reload()
    

    @property
    def justify(self):
        return self._justify
    
    @justify.setter
    def justify(self, value):
        self._justify = value
        if self.immediate_update:
            self.reload()
    

    @property
    def padding(self):
        return self._padding
    
    @padding.setter
    def padding(self, value):
        to_set = value
        if isinstance(value, str):
            vals = value.split(',')
            to_set = (vals[0], vals[1]) if len(vals) == 2 else (vals[0],vals[0])
        self._padding = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def relief(self):
        return self._relief
    
    @relief.setter
    def relief(self, value):
        self._relief = value
        if self.immediate_update:
            self.reload()
    

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        if self.immediate_update:
            self.reload()
    

    @property
    def take_focus(self):
        return self._take_focus
    
    @take_focus.setter
    def take_focus(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = bool(value)
        self._take_focus = to_set
        if self.immediate_update:
            self.reload()
    

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = str(value)
        if self.immediate_update:
            self.reload()
    

    @property
    def underline(self):
        return self._underline
    
    @underline.setter
    def underline(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._underline = to_set
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
    def wrap_length(self):
        return self._wrap_length
    
    @wrap_length.setter
    def wrap_length(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = int(value)
        self._wrap_length = to_set
        if self.immediate_update:
            self.reload()

    #endregion properties

    def backing_element_generator(self, parent):
        self.element = TK.Label(parent)
        self.reload()
        return self.element
    
    def reload(self):
        self.element.config(
                            activebackground=self.active_background,
                            activeforeground=self.active_foreground,
                            anchor=self.anchor,
                            background=self.background,
                            bitmap=self.bitmap,
                            borderwidth=self.border_width,
                            compound=self.compound,
                            cursor=self.cursor,
                            disabledforeground=self.disabled_foreground,
                            text=self.text,
                            font=(self.font_family, self.font_size),
                            foreground=self.foreground,
                            height=self.height,
                            highlightbackground=self.highlight_background,
                            highlightcolor=self.highlight_foreground,
                            highlightthickness=self.highlight_thickness,
                            image=self.image,
                            justify=self.justify,
                            padx=self.padding[0],
                            pady=self.padding[1],
                            relief=self.relief,
                            state=self.state,
                            takefocus=self.take_focus,
                            underline=self.underline,
                            width=self.width,
                            wraplength=self.wrap_length,
                        )

register_element("TextBlock", TextBlock)