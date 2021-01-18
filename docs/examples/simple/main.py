import xml.etree.cElementTree as ET
import tkinter as TK
import tkinter_xml.elements.Button
from tkinter_xml.Page import *


class MainPage(Page):
    def __init__(self, source):
        super().__init__(source, {}, [])
        self.window = TK.Tk()
        self.counter = 0
    
    def run(self):
        self.page_children[0].backing_element_generator(self.window).grid()
        self.window.mainloop()
    
    def other_click_fn(self, button):
        print("Oh yeah:", self, button)
        if button.foreground == "red":
            button.foreground = "black"
        else:
            button.foreground = "red"
        self.counter += 1
        self.should_be_visible_on_mainpage.text = str(self.counter)

main_window = MainPage("simple.xml")
main_window.run()