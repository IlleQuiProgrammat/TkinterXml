import xml.etree.cElementTree as ET
import tkinter as TK
import tkinter_xml.elements.Button
from tkinter_xml.Page import *
from tkinter_xml.element_list import register_element

class QuoteElement(Page):
    def __init__(self, attributes, children, parent_page, immediate_update=False):
        if len(children) != 0:
            raise Exception("QuoteElement cannot have any children")
        source = "./quote_element.xml"
        super().__init__(source, attributes, [], None)
    
    def onclick(self, quote_button):
        print(f"Clicked {self}")

register_element("QuoteElement", QuoteElement)

class MainPage(Page):
    def __init__(self, source):
        super().__init__(source, {}, [])
        self.window = TK.Tk()
        self.counter = 0
    
    def run(self):
        self.page_children[0].backing_element_generator(self.window).grid()
        self.window.mainloop()
    
    def change_collection(self, collection_button):
        collection_name = collection_button.text
        self.title.text = collection_name

main_window = MainPage("testing.xml")
main_window.run()