import tkinter as TK
import xml.etree.cElementTree as ET
import importlib
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.elements.Grid import *
from tkinter_xml.elements.Button import *
from tkinter_xml.elements.TextBlock import *

class Page(BaseElement):
    page_children = None
    def __init__(self, sourcefile, attributes, children, parent_page=None):
        self.default_attributes = {}
        super().__init__(attributes, children, self, False)
        self.sourcefile = sourcefile
        self.process_source()
    
    # TODO: Make this more generic
    def process_xml_tree(self, element_tree: [ET.Element]):
        element = element_tree[0]
        children = [self.process_xml_tree(child) for child in element_tree[1]]
        if element.tag == "Page":
            for attrib in element.attrib.keys():
                if attrib.startswith("include."):
                    alias = attrib[8:]
                    # TODO: set up proper importing
                    importlib.import_module(element.attrib[attrib])
                    alias = element.attrib[attrib]
            if self.page_children != None:
                raise Exception("Re-definition of page not permitted")
            self.page_children = children
            return self.page_children
        else:
            return eval(element.tag.replace(":", ".", 1))(element.attrib, children, self)

    def dfs_xml(self, element: ET.Element):
        currelem = [element]
        currelem.append([self.dfs_xml(child) for child in element])
        return currelem

    def process_source(self):
        root_tag = ET.ElementTree(file=self.sourcefile)
        result = self.dfs_xml(root_tag.getroot())
        self.process_xml_tree(result)
    
    def backing_element_generator(self, parent):
        return self.children[0].backing_element_generator(self).grid()