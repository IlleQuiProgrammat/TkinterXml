from tkinter_xml.Page import Page
import tkinter as TK

class SubPage(Page):
    def __init__(self, source, tk_parent_page):
        super().__init__(source, {}, [])
        self.tk_parent_page = tk_parent_page

    def launch(self):
        self.window = TK.Toplevel(self.tk_parent_page)
        self.page_children[0].backing_element_generator(self.window).grid()