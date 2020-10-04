import tkinter as TK
from tkinter_xml.elements.BaseElement import *

class Grid(BaseElement):

        
    # So that we can use type information to process the tree
    class ColumnDefinitions:
        def __init__(self, attributes, definitions, parent_page):
            self.definitions = definitions

    class RowDefinitions:
        def __init__(self, attributes, definitions, parent_page):
            self.definitions = definitions
            

    default_attributes = {
        "Background": "transparent"
    }
    
    def backing_element_generator(self, parent):
        grid_parent = TK.Frame(parent)

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
            grid_parent.grid_columnconfigure(index, weight=definition.multiplier, minsize=definition.minsize)
        for index, definition in enumerate(rows.definitions):
            grid_parent.grid_rowconfigure(index, weight=definition.multiplier, minsize=definition.minsize)
        
        for child in self.children:
            if not (isinstance(child, Grid.ColumnDefinitions) or isinstance(child, Grid.RowDefinitions)):
                column = 0
                row = 0
                if 'Grid' in child.custom_attributes:
                    if 'Column' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['Column'])
                    if 'Row' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['Row'])
                
                child.backing_element_generator(grid_parent).grid(column=column, row=row)
        return grid_parent


class ColumnDefinition(BaseElement):
    def __init__(self, attributes, children, parent_page):
        self.multiplier = 0
        self.minsize = 0
        definition = attributes["Width"]
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

class RowDefinition(BaseElement):
    def __init__(self, attributes, children, parent_page):
        definition = attributes["Height"]
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