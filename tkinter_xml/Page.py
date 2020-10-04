import tkinter as TK
import xml.etree.cElementTree as ET
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.elements.Grid import *
from tkinter_xml.elements.Button import *
from tkinter_xml.elements.TextBlock import *

class Page(BaseElement):
    page_children = None
    def __init__(self, sourcefile, attributes, children, parent_page=None):
        super().__init__(attributes, children, self)
        self.sourcefile = sourcefile
        self.process_source()
    
    # TODO: Make this more generic
    def process_xml_tree(self, element_tree: [ET.Element]):
        element = element_tree[0]
        children = [self.process_xml_tree(child) for child in element_tree[1]]
        print(children)
        if element.tag == "Page":
            if self.page_children != None:
                raise Exception("Re-definition of page not permitted")
            self.page_children = children
            return self.page_children
        elif element.tag == "Button":
            # create a button here
            return Button(element.attrib, children, self)
        elif element.tag == "TextBlock":
            # create a label here
            return TextBlock(element.attrib, children, self)
        elif element.tag == "Grid":
            return Grid(element.attrib, children, self)
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

    def dfs_xml(self, element: ET.Element):
        currelem = [element]
        currelem.append([self.dfs_xml(child) for child in element])
        return currelem

    def process_source(self):
        root_tag = ET.ElementTree(file=self.sourcefile)
        result = self.dfs_xml(root_tag.getroot())
        self.process_xml_tree(result)
    
    def backing_element_generator(self, parent):
        return children[0].backing_element_generator(self).grid()