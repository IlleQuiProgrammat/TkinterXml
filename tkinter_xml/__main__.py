import xml.etree.cElementTree as ET
import tkinter as TK
from tkinter_xml.elements.Grid import *
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.elements.Button import *
from tkinter_xml.elements.TextBlock import *
class MainPage:
    def __init__(self, childlist):
        if len(childlist) != 1:
            raise Exception("MainPage must have exactly one child")
        self.child = childlist[0]
        self.window = TK.Tk()
    
    def run(self):
        self.child.backing_element_generator(self.window).grid()
        self.window.mainloop()

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