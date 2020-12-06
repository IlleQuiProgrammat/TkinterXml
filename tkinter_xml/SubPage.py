from tkinter_xml.Page import Page
import tkinter as TK

class SubPage(Page):
    """Allows creation of sub-windows
    This is achieved by creating a ``tkinter.Toplevel`` element bound to
    ``tk_parent_page``. The subpage also calls the constructor of
    ``tkinter_xml.Page`` in order to parse the document.
    
    :param source: the xml file describing the subpage's contents
    :param tk_parent_page: the tkinter window that the toplevel is spawned from
    """

    def __init__(self, source: str, tk_parent_page: TK.Tk):
        """Constructor method"""

        super().__init__(source, {}, [])
        self.tk_parent_page = tk_parent_page

    def launch(self):
        """Spawns the top level element and binds the child xml element to it"""

        self.window = TK.Toplevel(self.tk_parent_page)
        self.page_children[0].backing_element_generator(self.window).grid()
    
    def close(self, *args, **kwargs):
        """Closes the subpage that was created

        :param \*args: Accepts an arbitrary number of arguments so that it can be \
            called from a button for example
        :param \*\*kwards: See ``*args``
        """

        self.window.destroy()