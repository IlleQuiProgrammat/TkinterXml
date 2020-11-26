import tkinter as TK
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.element_list import register_element


class Grid(BaseElement):

        
    # So that we can use type information to process the tree
    class ColumnDefinitions:
        def __init__(self, attributes, definitions, parent_page):
            self.definitions = definitions
            if "x_Name" in attributes:
                setattr(parent_page, attributes["x_Name"], self)

    class RowDefinitions:
        def __init__(self, attributes, definitions, parent_page):
            self.definitions = definitions
            if "x_Name" in attributes:
                setattr(parent_page, attributes["x_Name"], self)
            
    def __init__(self, attributes, children, parent_page):
        self._background = "#E4E4E4"
        
        super().__init__(attributes, children, parent_page, False)
    
    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = value
        if self.immediate_update:
            self.reload()

    def backing_element_generator(self, parent):
        grid_parent = TK.Frame(parent)
        self.element = grid_parent
        self.reload()
        return grid_parent
    
    def reload(self):
        self.element.config(background=self.background)
        

        # Collect row definitions from anywhere in a direct child xml node and use the {Column,Row}Definition class to
        # parse them
        columns = None
        rows = None
        for child in self.children:
            if isinstance(child, Grid.ColumnDefinitions):
                if columns != None:
                    raise Exception("Grid element cannot have more than 1 column definition")
                columns = child
            if isinstance(child, Grid.RowDefinitions):
                if rows != None:
                    raise Exception("Grid element cannot have more than 1 row definition")
                rows = child

        # If none are found, default to none so we dont get a NoneType error
        if rows == None:
            rows = Grid.RowDefinitions({}, [], None)
        if columns == None:
            columns = Grid.ColumnDefinitions({}, [], None)
        
        # Configure the columns and rows based on the parsed values
        for index, definition in enumerate(columns.definitions):
            self.element.grid_columnconfigure(index, weight=definition.multiplier, minsize=definition.minsize)
        for index, definition in enumerate(rows.definitions):
            self.element.grid_rowconfigure(index, weight=definition.multiplier, minsize=definition.minsize)
        
        for child in self.children:
            if not (isinstance(child, Grid.ColumnDefinitions) or isinstance(child, Grid.RowDefinitions)):
                column = 0
                row = 0
                if 'Grid' in child.custom_attributes:
                    if 'column' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['column'])
                    if 'row' in child.custom_attributes['Grid']:
                        row = int(child.custom_attributes['Grid']['row'])
                
                child.backing_element_generator(self.element).grid(column=column, row=row)

register_element("Grid", Grid)
register_element("Grid.RowDefinitions", Grid.RowDefinitions)
register_element("Grid.ColumnDefinitions", Grid.ColumnDefinitions)

class ColumnDefinition(BaseElement):
    def __init__(self, attributes, children, parent_page):
        self.multiplier = 0
        self.minsize = 0
        definition = attributes["width"]
        if '*' in definition:
            preparsed = definition.split("*")
            parsed = []
            for v in parsed:
                if v != '':
                    parsed.append(v)
            if len(parsed) > 1 or (len(parsed) == 1 and parsed[0].isdigit()):
                raise Exception(f"ColumnDefinition `{definition}' is invalid")
            self.multiplier = 1
            if len(parsed) == 1:
                self.multiplier = int(parsed[0])
        else:
            if not definition.isdigit():
                raise Exception(f"ColumnDefinition `{definition}' is invalid")
            self.minsize = int(definition)

register_element("ColumnDefinition", ColumnDefinition)

class RowDefinition(BaseElement):
    def __init__(self, attributes, children, parent_page):
        definition = attributes["height"]
        self.multiplier = 0
        self.minsize = 0
        if '*' in definition:
            preparsed = definition.split("*")
            parsed = []
            for v in parsed:
                if v != '':
                    parsed.append(v)
            if len(parsed) > 1 or (len(parsed) == 1 and parsed[0].isdigit()):
                raise Exception(f"RowDefinition `{definition}' is invalid")
            self.multiplier = 1
            if len(parsed) == 1:
                self.multiplier = int(parsed[0])
        else:
            if not definition.isdigit():
                raise Exception(f"RowDefinition `{definition}' is invalid")
            self.minsize = int(definition)

register_element("RowDefinition", RowDefinition)