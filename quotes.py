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
    
    def change_collection(self, collection_button):
        collection_name = collection_button.content
        self.title.text = collection_name

main_window = MainPage("testing.xml")
main_window.run()