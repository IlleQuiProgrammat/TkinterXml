import xml.etree.cElementTree as ET
import tkinter as TK
import tkinter_xml.elements.Button
from tkinter_xml.Page import *
from tkinter_xml.element_list import register_element
from tkinter_xml.SubPage import SubPage
from tkinter_xml.elements.InputBox import InputBox

class QuoteElement(Page):
    def __init__(self, attributes, children, parent_page, immediate_update=False):
        if len(children) != 0:
            raise Exception("QuoteElement cannot have any children")
        source = "./quote_element.xml"
        super().__init__(source, attributes, [], None)
    
    @property
    def quote_text(self):
        return self.quote_label.text
    
    @quote_text.setter
    def quote_text(self, value):
        if hasattr(self.quote_label, "element"):
            self.quote_label.text = value
        else:
            self.quote_label._text = value

    def delete(self, quote_button):
        print(f"Attempted to delete {self}")
        del self

register_element("QuoteElement", QuoteElement)

class TestPage(SubPage):
    def __init__(self, tk_parent_page, title, valid_quotes):
        super().__init__("./test_subpage.xml", tk_parent_page)
        self.title = ""
        self.correct_quotes = []
        self.valid_quotes = []
    
    def check_answer(self, button):
        if self.input_box.content in self.correct_quotes:
            self.message.text = "You've already input that one before!"
        elif self.input_box.content in self.valid_quotes:
            self.correct_quotes.append(self.input_box.content)
            self.input_box.content = ""
            self.message.text = "Correct!"
        else:
            self.input_box.content = ""
            self.message.text = "Wrong :("

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
        self.tp = TestPage(self.window, "title", ["halo"])
        self.tp.launch()

main_window = MainPage("testing.xml")
main_window.run()