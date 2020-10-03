import xml.etree.cElementTree as ET
import tkinter as TK

class BaseElement():
    def render(self, window):
        ...

    def get_renderable(self):
        ...


class MainPage:
    def __init__(self, childlist):
        if len(childlist) != 1:
            raise Exception("MainPage must have exactly one child")
        self.child = childlist[0]
        self.window = TK.Tk()
    
    def run(self):
        self.child.backing_element_generator(self.window).grid()
        self.window.mainloop()

class Grid(BaseElement):
    default_attributes = {
        "Background": "transparent"
    }
    def __init__(self, attributes, children):
        for attribute in attributes.keys():
            if attribute not in self.default_attributes:
                raise Exception(f"Encountered an invalid attribute on TextBlock: {attribute}")
            else:
                self.default_attributes[attribute] = attributes[attribute]
        self.children = children
    
    def backing_element_generator(self, parent):
        grid_parent = TK.Frame(parent)
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
        if rows == None:
            rows = RowDefinitions([])
        if columns == None:
            columns = ColumnDefinitions([])
        # TODO: refactor into the column and row definition classes
        for index, definition in enumerate(columns.definitions):
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
                    raise Exception(f"RowDefinition {definition} is invalid")
                minsize = int(definition)
            grid_parent.grid_columnconfigure(index, weight=multiplier, minsize=minsize)
        for index, definition in enumerate(rows.definitions):
            multiplier = 0
            minsize = 0
            if '*' in definition:
                parsed = definition.split("*")
                if len(parsed) > 1 or (len(parsed) == 1 and parsed[0].isdigit()):
                    raise Exception(f"RowDefinition `{definition}' is invalid")
                multiplier = 1
                if len(parsed) == 1:
                    multiplier = int(parsed[0])
            else:
                if not parsed.isdigit():
                    raise Exception(f"RowDefinition {definition} is invalid")
                minsize = int(parsed)
            grid_parent.grid_rowconfigure(index, weight=multiplier, minsize=minsize)
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
        self.definitions = definitions

class RowDefinitions:
    def __init__(self, definitions):
        self.definitions = definitions


class TextBlock(BaseElement):
    default_attributes = {
        "Text": "",
        "FontSize": 12,
        "FontFamily": "Segoe UI",
        "Foreground": "black"
    }
    custom_attributes = {}
    def __init__(self, attributes, children):
        for attribute in attributes.keys():
            if '.' in attribute:
                custom_attribute_prefix = attribute.split('.')[0]
                if custom_attribute_prefix in self.custom_attributes:
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                else:
                    self.custom_attributes[custom_attribute_prefix] = {}
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                continue
            if attribute not in self.default_attributes:
                raise Exception(f"Encountered an invalid attribute on TextBlock: {attribute}")
            else:
                self.default_attributes[attribute] = attributes[attribute]
        self.backing_element_generator = self.generate_backing_element()
    
    def generate_backing_element(self):
        return lambda parent: TK.Label(parent,
                                        text=self.default_attributes["Text"],
                                        font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                        foreground=self.default_attributes["Foreground"]
                                )

EVENT_HANDLERS = {'Click'}

def other_click_fn(b):
    print("hello", b)

class Button(BaseElement):
    default_attributes = {
        "Content": "Button",
        "FontSize": 12,
        "FontFamily": "Segoe UI",
        "Foreground": "black",
        "Click": lambda s: print("Button clicked"),
    }
    custom_attributes = {}
    def __init__(self, attributes, children):
        for attribute in attributes.keys():
            if '.' in attribute:
                custom_attribute_prefix = attribute.split('.')[0]
                if custom_attribute_prefix in self.custom_attributes:
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                else:
                    self.custom_attributes[custom_attribute_prefix] = {}
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                continue
            if attribute not in self.default_attributes:
                raise Exception(f"Encountered an invalid attribute on Button: {attribute}")
            else:
                if attribute in EVENT_HANDLERS:
                    self.default_attributes[attribute] = eval(attributes[attribute])
                else:
                    self.default_attributes[attribute] = attributes[attribute]
                
        self.backing_element_generator = self.generate_backing_element()
    
    def generate_backing_element(self):
        return lambda parent: TK.Button(parent,
                                        text=self.default_attributes["Content"],
                                        font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                        foreground=self.default_attributes["Foreground"],
                                        command=lambda: self.default_attributes["Click"](self)
                                )

main_window = None

# TODO: Make generic
def process(element_tree: [ET.Element]):
    print(element_tree)
    global main_window
    element = element_tree[0]
    children = [process(child) for child in element_tree[1]]
    print(children)
    if element.tag == "Page":
        if main_window != None:
            raise Exception("Re-definition of page not permitted")
        main_window = MainPage(children)
        return main_window
    elif element.tag == "Button":
        # create a button here
        return Button(element.attrib, children)
    elif element.tag == "TextBlock":
        # create a label here
        return TextBlock(element.attrib, children)
    elif element.tag == "Grid":
        return Grid(element.attrib, children)
    elif element.tag == "Grid.ColumnDefinitions":
        return ColumnDefinitions(children)
    elif element.tag == "ColumnDefinition":
        return element.attrib["Width"]
    elif element.tag == "Grid.RowDefinitions":
        return RowDefinitions(children)
    elif element.tag == "RowDefinition":
        return element.attrib["Height"]
    else:
        raise Exception("Invalid tag")


def dfs(element: ET.Element):
    currelem = [element]
    currelem.append([dfs(child) for child in element])
    return currelem

root_tag = ET.ElementTree(file="simple.xml")
result = dfs(root_tag.getroot())
process(result)
main_window.run()