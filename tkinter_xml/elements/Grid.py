import tkinter as TK
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.element_list import register_element


class Grid(BaseElement):
    """Represents a tkinter frame element which grids its children based on custom attributes and col/row definitions

    Example:

    .. highlight:: xml
    .. code-block:: xml

        <Grid>
            <!-- This is not rendered but is used to set the definitions, Grid.ColumnDefinitions is similarly used -->
            <Grid.RowDefinitions>
                <RowDefinition height="20" />
                <RowDefinition height="*" /> <!-- Row size adapts to largest of its children -->
            </Grid.RowDefinitions>
            <!-- Example usage of the custom attribute to define the row -->
            <Button Grid.row="0" text="button" />
            <Button Grid.row="1" text="button2" height="50"/>
        </Grid>
    
    .. note: all properties are directly set to their corresponding tkinter properties. These are often just their names
        without the underscores
    """
    class ColumnDefinitions:
        """Stores the definitions so that they can be parsed from xml
        
        .. note: although it may seem odd, ``x_Name`` is a supported tag and is supported so that modifying the grid
            using code is less cumbersome.

        :param definitions: Normally the children, this time they are treated as being ``ColumnDefinition`` only
        :type definitions: List[ColumnDefinition]
        """

        def __init__(self, attributes, definitions, parent_page):
            self.definitions = definitions
            if "x_Name" in attributes:
                setattr(parent_page, attributes["x_Name"], self)

    class RowDefinitions:
        """Stores the definitions so that they can be parsed from xml
        
        .. note: although it may seem odd, ``x_Name`` is a supported tag and is supported so that modifying the grid
            using code is less cumbersome.

        :param definitions: Normally the children, this time they are treated as being ``RowDefinition`` only
        :type definitions: List[RowDefinition]
        """

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
        self.__prev_children = []
        self.reload()
        return grid_parent
    
    def reload(self):
        """Defines the configuration of the grid
        
        :raises: Exception for the following:
             * More than one ``Grid.ColumnDefinition`` child
             * More than one ``Grid.RowDefinition`` child
        """

        self.element.config(background=self.background)
        
        # Remove the old elements so that they don't remain in the grid if one happens to be removed
        for oldchild in self.__prev_children:
            if isinstance(oldchild, BaseElement) and hasattr(oldchild, "element"):
                oldchild.element.destroy()

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
                if 'Grid' in child.custom_attributes:  # parse the position from the `Grid.<>` attributes
                    if 'column' in child.custom_attributes['Grid']:
                        column = int(child.custom_attributes['Grid']['column'])
                    if 'row' in child.custom_attributes['Grid']:
                        row = int(child.custom_attributes['Grid']['row'])
                
                child.backing_element_generator(self.element).grid(column=column, row=row)  # render the element
        self.__prev_children = self.children  # store the current children so that we can handle deleting of children

register_element("Grid", Grid)
register_element("Grid.RowDefinitions", Grid.RowDefinitions)
register_element("Grid.ColumnDefinitions", Grid.ColumnDefinitions)

class ColumnDefinition(BaseElement):
    """Defines the columns of grid for parsing from xml
        
        :raises: Exception when the column definition is invalid

        :param attributes: should only contain min width integer or multiplier followed by a ``*`` such as ``2*`` as per
            tkinter ``.grid_columnconfigure()`` method on widgets.
    """

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
    """Defines the row of grid parsing from xml
        
        :raises: Exception when the row definition is invalid

        :param attributes: should only contain min width integer or multiplier followed by a ``*`` such as ``2*`` as per
            tkinter ``.grid_rowconfigure()`` method on widgets.
    """
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