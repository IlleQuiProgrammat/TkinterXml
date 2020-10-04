import tkinter as TK
from tkinter_xml.elements.BaseElement import *

class Grid(BaseElement):
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
            if isinstance(child, ColumnDefinitions):
                if columns != None:
                    raise Exception("Grid element cannot have more than 1 column definition")
                columns = child
            if isinstance(child, RowDefinitions):
                if rows != None:
                    raise Exception("Grid element cannot have more than 1 row definition")
                rows = child

        # If none are found, default to none so we dont get a NoneType error
        if rows == None:
            rows = RowDefinitions([])
        if columns == None:
            columns = ColumnDefinitions([])
        
        # Configure the columns and rows based on the parsed values
        for index, definition in enumerate(columns.definitions):
            grid_parent.grid_columnconfigure(index, weight=definition[0], minsize=definition[0])
        for index, definition in enumerate(rows.definitions):
            grid_parent.grid_rowconfigure(index, weight=definition[0], minsize=definition[1])
        
        for child in self.children:
            if not (isinstance(child, ColumnDefinitions) or isinstance(child, RowDefinitions)):
                column = 0
                row = 0
                if 'Grid' in child.custom_attributes:
                    if 'Column' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['Column'])
                    if 'Row' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['Row'])
                
                child.backing_element_generator(grid_parent).grid(column=column, row=row)
        return grid_parent

# So that we can use type information to process the tree
class ColumnDefinitions:
    def __init__(self, definitions):
        self.definitions = []
        for definition in definitions:
            self.definitions.append(self.parse_column_definition(definition))

    def parse_column_definition(self, definition):
        multiplier = 0
        minsize = 0
        if '*' in definition:
            preparsed = definition.split("*")
            parsed = []
            for v in parsed:
                if v != '':
                    parsed.append(v)
            if len(parsed) > 1 or (len(parsed) == 1 and parsed[0].isdigit()):
                raise Exception(f"ColumnDefinition `{definition}' is invalid")
            multiplier = 1
            if len(parsed) == 1:
                multiplier = int(parsed[0])
        else:
            if not definition.isdigit():
                raise Exception(f"ColumnDefinition {definition} is invalid")
            minsize = int(definition)
        return (multiplier, minsize)

class RowDefinitions:
    def __init__(self, definitions):
        self.definitions = []
        for definition in definitions:
            self.definitions.append(self.parse_row_definition(definition))

    def parse_row_definition(self, definition):
        multiplier = 0
        minsize = 0
        if '*' in definition:
            preparsed = definition.split("*")
            parsed = []
            for v in parsed:
                if v != '':
                    parsed.append(v)
            if len(parsed) > 1 or (len(parsed) == 1 and parsed[0].isdigit()):
                raise Exception(f"RowDefinition `{definition}' is invalid")
            multiplier = 1
            if len(parsed) == 1:
                multiplier = int(parsed[0])
        else:
            if not definition.isdigit():
                raise Exception(f"RowDefinition `{definition}' is invalid")
            minsize = int(definition)
        return (multiplier, minsize)