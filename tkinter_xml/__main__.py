import xml.etree.cElementTree as ET
import tkinter as TK
from tkinter_xml.Page import *
class MainPage(Page):
    def __init__(self, source):
        super().__init__(source, {}, [])
        self.window = TK.Tk()
    
    def run(self):
        self.page_children[0].backing_element_generator(self.window).grid()
        print(self.should_be_visible_on_mainpage)
        self.window.mainloop()
    
    def other_click_fn(self, button):
        print("Oh yeah:", self, button)

main_window = MainPage("simple.xml")
main_window.run()