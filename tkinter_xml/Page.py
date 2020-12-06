import tkinter as TK
import xml.etree.cElementTree as ET
from typing import List
from tkinter_xml.elements.BaseElement import *
from tkinter_xml.elements.Grid import *
from tkinter_xml.elements.Button import *
from tkinter_xml.elements.TextBlock import *
from tkinter_xml.element_list import retrieve_element

class Page(BaseElement):
    """Contains code to parse and create elements as well as render itself

    .. note:: Rendering always renders the first child element in xml, meaning that a grid \
        should be used if you want several child elements on a page element.

    :param sourcefile: the xml document to create the page from
    :param attributes: the xml attributes for the page which will be initialised by ``BaseElement``
    :param children: List of xml children elements which is required for parsing generically, though this can be \
        configured so that the children are used inside the element by a derived Page i.e. a custom component.
    :param parent_page: The page which the custom component is called from. This is used again for being able to \
        generically instantiate custom components but ``self.custom_element_parent`` is assigned this value in case
        there is a need to access it in a custom component. 
    """

    def __init__(self, sourcefile: str, attributes, children: List[BaseElement], parent_page=None):
        """Constructor Method"""

        self.page_children = None
        self.default_attributes = {}
        self.sourcefile = sourcefile
        self.custom_element_parent = parent_page
        self.process_source()
        super().__init__(attributes, children, self, False)
    
    def process_xml_tree(self, element_tree: List[ET.Element]):
        """Recursively processes the element tree retrieved from the depth-first-search

        The process in which this is done is as follows:
         * call ``process_xml_tree`` on all of the children of the current node
         * then instantiate a ``BaseElement``-derived class from the xml tag name, passing the attributes and children\
             along with the parent class.
         * return the root element from the xml tree - all the children will now have been instantiated, but they will\
             not know who the parent is - this will be handled when we process the rendering
        
        :param element_tree: A tuple of ``(xml.etree.cElementTree.Element, List[T])`` Where the list is the same \
            type as the element tree itself.
        """

        element = element_tree[0]
        children = [self.process_xml_tree(child) for child in element_tree[1]]
        if element.tag == "Page":
            if self.page_children != None:
                raise Exception("Re-definition of page not permitted")
            self.page_children = children
            return self.page_children
        else:
            return retrieve_element(element.tag.replace(":", ".", 1))(element.attrib, children, self)

    def dfs_xml(self, element: ET.Element):
        """Preprocesses the element tree using dfs so that it is easier to handle"""

        currelem = [element]
        currelem.append([self.dfs_xml(child) for child in element])
        return currelem

    def process_source(self):
        """Loads the source file and processes it"""

        root_tag = ET.ElementTree(file=self.sourcefile)
        result = self.dfs_xml(root_tag.getroot())
        self.process_xml_tree(result)
    
    def backing_element_generator(self, parent):
        """Overloads the default element generator to refer to its first child
        
        :param parent: tkinter widget
        """

        self.element = self.page_children[0].backing_element_generator(parent)
        return self.element