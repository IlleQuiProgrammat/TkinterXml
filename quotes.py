import xml.etree.cElementTree as ET
import tkinter as TK
import tkinter_xml.elements.Button
from tkinter_xml.Page import *
from tkinter_xml.element_list import register_element
from quote_lib.main import ApplicationRepresentation

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

class MainPage(Page):
    def __init__(self, source):
        super().__init__(source, {}, [])
        self.application_representation = ApplicationRepresentation()
        self.window = TK.Tk()
    
    def run(self):
        for i, collection in enumerate(self.application_representation.collections):
            self.collection_grid_rowdefinitions.definitions.append(
                RowDefinition({"height": "30"}, [], self)
            )
            self.collection_grid.children.append(Button({
                "Grid.row": str(i),
                "text": collection.name,
                "font_size": "16",
                "click": "change_collection",
                "width": "15",
                "Collection.id": str(i),
            }, [], self, True))
        self.page_children[0].backing_element_generator(self.window).grid()
        self.window.mainloop()
    
    def change_collection(self, collection_button):
        collection_id = int(collection_button.custom_attributes["Collection"]["id"])
        self.current_collection = self.application_representation.collections[collection_id]
        self.reload_collection()        
    
    def reload_collection(self):
        for i, quote in enumerate(self.current_collection.quotes):
            self.quote_grid_rowdefinitions.definitions.append(
                RowDefinition({"height": "30"}, [], self)
            )
            self.quote_grid.children.append(QuoteElement({
                "Grid.row": str(i),
                "quote_text": quote.phrase
            }, [], self, True))
        self.quote_grid.reload()

main_window = MainPage("testing.xml")
main_window.run()