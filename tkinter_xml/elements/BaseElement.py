import tkinter as TK

class BaseElement():
    """Determines the parsing of elements from their xml and provides a generic interface for handling elements

    .. warning: As the parsing of the xml occurs on the fly, there is a chance that errors will not be caught by simply 
        running the program.

    :param attributes: the xml attributes, these will be assigned to the derived class instance using ``setattr``, \
        ``x_Name`` will set a variable on the ``parent_page`` class instance allowing the element to be accessed through
        code without having to traverse the xml tree.
    :param children: a list containing the child xml elements, required for the rendering process
    :type children: List[BaseElement]
    :param parent_page: the page on which attributes should be set
    :type parent_page: Page
    :param immediate_update: sets whether the widget should update on every property change or only when the user
        manually calls ``.reload()``
    :type immediate_update: bool
    """

    def __init__(self, attributes, children, parent_page, immediate_update):
        self.custom_attributes = {}
        self.immediate_update = False
        self.children = children
        self.parent_page = parent_page
        attributes = {a.strip() : attributes[a].strip() for a in attributes}
        if "x_Name" in attributes:
                setattr(parent_page, attributes["x_Name"], self)
        for attribute in attributes.keys():
            if 'x_Name' == attribute:
                continue
            elif '.' in attribute:
                custom_attribute_prefix = attribute.split('.')[0]
                if custom_attribute_prefix in self.custom_attributes:
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
                else:
                    self.custom_attributes[custom_attribute_prefix] = {}
                    self.custom_attributes[custom_attribute_prefix][".".join(attribute.split('.')[1:])] = attributes[attribute]
            elif attribute not in dir(self):
                raise Exception(f"{self} missing {attribute} ({dir(self)})")
            else:
                setattr(self, attribute, attributes[attribute])
        self.immediate_update = immediate_update
    
    def backing_element_generator(self, parent):
        """Provides a default element generator which returns an empty frame
        
        :param parent: tkinter widget
        """
        return TK.Frame()
    
    def reload(self):
        """Updates the element using ``.config()`` with potentially changed properties"""
        pass