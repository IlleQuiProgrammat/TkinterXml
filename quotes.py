from quote_lib.collection import QuoteCollection
from typing import List
from quote_lib.quote import Quote, get_quote, get_quote_fuzzy
import xml.etree.cElementTree as ET
import tkinter as TK
import random
import tkinter_xml.elements.Button
from tkinter_xml.Page import *
from tkinter_xml.element_list import register_element
from tkinter_xml.SubPage import SubPage
from tkinter_xml.elements.InputBox import InputBox
from quote_lib.main import ApplicationRepresentation

class QuoteElement(Page):
    def __init__(self, attributes, children, parent_page, immediate_update=False):
        if len(children) != 0:
            raise Exception("QuoteElement cannot have any children")
        source = "./quote_element.xml"
        super().__init__(source, attributes, [], parent_page)
    
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
        index = [quote.phrase for quote in self.custom_element_parent.current_collection.quotes].index(self.quote_text)
        self.custom_element_parent.current_collection.quotes.pop(index)
        print(self.custom_element_parent.current_collection.quotes)
        self.custom_element_parent.reload_collection()

register_element("QuoteElement", QuoteElement)

class TestPage(SubPage):
    def __init__(self, tk_parent_page, title, valid_quotes: List[Quote]):
        super().__init__("./test_subpage.xml", tk_parent_page)
        self.title = title
        self.correct_quotes = []
        self.valid_quotes = valid_quotes

    def check_quote(self, button):
        quote = None
        if self.input_box.content in [q.phrase for q in self.correct_quotes]:
            self.message.text = "You've already input that one before!"
        else:
            quote = get_quote_fuzzy(self.input_box.content, self.valid_quotes, 0.9)
            if quote:
                self.correct_quotes.append(quote)
                self.input_box.content = ""
                self.message.text = "Correct!"
                quote.correct += 1
            else:
                self.message.text = "Wrong :("
    
    def launch(self):
        super().launch()
        self.test_title.text = self.title

    def complete_test(self, button):
        res = ResultsPage(self.tk_parent_page, "", self.correct_quotes, self.valid_quotes)
        res.launch()
        self.close()

class ResultsPage(SubPage):
    def __init__(self, tk_parent_page, title, correct_quotes, valid_quotes):
        super().__init__("./results_subpage.xml", tk_parent_page)
        correct_set = set(correct_quotes)
        for i, quote in enumerate(valid_quotes):
            self.quote_grid_rowdefinitions.definitions.append(
                RowDefinition({"height": "30"}, [], self)
            )
            self.quote_grid.children.append(TextBlock({
                "Grid.row": str(i),
                "text": ("Correct: " if get_quote(quote.phrase, correct_quotes) else "Incorrect: ") + quote.phrase,
            }, [], self, True))
            if quote in correct_set:
                quote.available += 1
        
class AddQuotePage(SubPage):
    def __init__(self, tk_parent_page, collection: QuoteCollection, parent):
        super().__init__("./addquote_subpage.xml", tk_parent_page)
        self.collection = collection
        self.parent = parent

    def add_new_quote(self, button):
        phrase = self.phrase_input.content
        tags = [tag.strip() for tag in self.tag_input.content.split(",")]
        self.collection.quotes.append(Quote({"phrase": phrase, "tags": tags, "available": 0, "correct": 0}))
        self.close()
        self.parent.reload_collection()
        

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
        self.application_representation.save()
    
    def change_collection(self, collection_button):
        collection_name = collection_button.text
        self.title.text = collection_name
        collection_id = int(collection_button.custom_attributes["Collection"]["id"])
        self.current_collection = self.application_representation.collections[collection_id]
        self.reload_collection()
    
    def run_test(self, button):
        tag = random.choice(self.current_collection.tags)
        tags = []
        for q in self.current_collection.quotes:
            if tag in q.tags:
                tags.append(q)
        self.tp = TestPage(self.window, f"{self.current_collection.name} - {tag} test", tags)
        self.tp.launch()
    
    def reload_collection(self):
        self.quote_grid_rowdefinitions.definitions = []
        res = []
        for element in self.quote_grid.children:
            if isinstance(element, Grid.RowDefinitions) or isinstance(element, Grid.ColumnDefinitions):
                res.append(element)
        self.quote_grid.children = res
        for i, quote in enumerate(self.current_collection.quotes):
            self.quote_grid_rowdefinitions.definitions.append(
                RowDefinition({"height": "30"}, [], self)
            )
            self.quote_grid.children.append(QuoteElement({
                "Grid.row": str(i),
                "quote_text": quote.phrase
            }, [], self, True))
        print(self.quote_grid.children)
        self.quote_grid.reload()
    
    def add_quote(self, button):
        qw = AddQuotePage(self.window, self.current_collection, self)
        qw.launch()


main_window = MainPage("testing.xml")
main_window.run()