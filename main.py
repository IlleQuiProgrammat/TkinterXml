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
        self.child.backing_element_generator(self.window)
        self.window.mainloop()

class Grid(BaseElement):
    def __init__(self):
        ...

class TextBlock(BaseElement):
    default_attributes = {
        "Text": "",
        "FontSize": 12,
        "FontFamily": "Segoe UI",
        "Foreground": "black"
    }
    def __init__(self, attributes, children):
        for attribute in attributes.keys():
            if attribute not in self.default_attributes:
                raise Exception(f"Encountered an invalid attribute on TextBlock {attribute}")
            else:
                self.default_attributes[attribute] = attributes[attribute]
        self.backing_element_generator = self.generate_backing_element()
    
    def generate_backing_element(self):
        return lambda parent: TK.Label(parent,
                                        text=self.default_attributes["Text"],
                                        font=(self.default_attributes["FontFamily"], self.default_attributes["FontSize"]),
                                        foreground=self.default_attributes["Foreground"]
                                ).grid()
        
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
        return
    elif element.tag == "TextBlock":
        # create a label here
        return TextBlock(element.attrib, children)
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