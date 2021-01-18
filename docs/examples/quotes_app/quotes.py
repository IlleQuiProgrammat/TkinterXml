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
    """Represents a quote custom control with the ability to delete itself"""

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
        if hasattr(self.quote_label, "element"):  # if the element has already been rendered and can hence be updated
            self.quote_label.text = value
        else:  # otherwise, modify the initial default value so that it is used on creation.
            self.quote_label._text = value

    def delete(self, quote_button):
        """Deletes the current quote from the parent quote collection"""
        
        index = [quote.phrase for quote in self.custom_element_parent.current_collection.quotes].index(self.quote_text)
        self.custom_element_parent.current_collection.quotes.pop(index)  # remove the element
        self.custom_element_parent.reload_collection()  # reload the collection to update the ui and remove this element

register_element("QuoteElement", QuoteElement)  # make sure that the element is accessible from the xml parser

class TestPage(SubPage):
    def __init__(self, tk_parent_page, title, valid_quotes: List[Quote]):
        super().__init__("./test_subpage.xml", tk_parent_page)
        self.title = title
        self.correct_quotes = []
        self.valid_quotes = valid_quotes

    def check_quote(self, button):
        """Handles the user entering a new quote"""

        quote = None
        if get_quote_fuzzy(self.input_box.content, self.correct_quotes, 0.9):  # check if something similar has been entered
            self.message.text = "You've already input that one before!"
        else:
            quote = get_quote_fuzzy(self.input_box.content, self.valid_quotes, 0.9) # check if the quote is valid
            if quote:  # true when quote is found in valid_quotes and it has not already been said
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
        """Creates a results page and closes this test window so that more answers can't be entered"""

        res = ResultsPage(self.tk_parent_page, "", self.correct_quotes, self.valid_quotes)
        res.launch()
        self.close()

class ResultsPage(SubPage):
    """Presents a list of correct/missed quotes from the previous test"""

    def __init__(self, tk_parent_page, title, correct_quotes, valid_quotes):
        super().__init__("./results_subpage.xml", tk_parent_page)
        correct_set = set(correct_quotes)
        
        for i, quote in enumerate(valid_quotes):
            # Add results to a grid
            self.quote_grid_rowdefinitions.definitions.append(
                RowDefinition({"height": "30"}, [], self)
            )
            self.quote_grid.children.append(TextBlock({
                "Grid.row": str(i),
                "text": ("Correct: " if quote in correct_set else "Incorrect: ") + quote.phrase,
            }, [], self, True))
            if quote not in correct_set:
                quote.available += 1
        
class AddQuotePage(SubPage):
    def __init__(self, tk_parent_page, collection: QuoteCollection, parent):
        super().__init__("./addquote_subpage.xml", tk_parent_page)
        self.collection = collection
        self.parent = parent

    def add_new_quote(self, button):
        """Adds the entered quote to the parent collection and reloads the UI to handle the change"""

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
        for i, collection in enumerate(self.application_representation.collections):  # insert buttons onto side nav
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
        self.application_representation.save()  # save any changes saved in memory during program execution
    
    def change_collection(self, collection_button):
        """Switches the current visible collection by button text and updates the UI"""

        collection_name = collection_button.text
        self.title.text = collection_name
        collection_id = int(collection_button.custom_attributes["Collection"]["id"])
        self.current_collection = self.application_representation.collections[collection_id]
        self.reload_collection()
    
    def run_test(self, button):
        """Launches a test on a random tag for the given collection"""

        tag = random.choice(self.current_collection.tags)
        tags = []
        for q in self.current_collection.quotes:
            if tag in q.tags:
                tags.append(q)
        self.tp = TestPage(self.window, f"{self.current_collection.name} - {tag} test", tags)
        self.tp.launch()
    
    def reload_collection(self):
        """Updates the collection UI to match the current quotes in the collection"""

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
        
        self.quote_grid.reload()
    
    def add_quote(self, button):
        qw = AddQuotePage(self.window, self.current_collection, self)
        qw.launch()


main_window = MainPage("testing.xml")
main_window.run()