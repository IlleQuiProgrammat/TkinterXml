# TkinterXml

A Program designed to parse the tree of a XML document and render the result 
using tkinter


# Brief Documentation

The syntax for the XML is standard XML but currently there are few currently 
supported tags.

1. `Page` - can only be defined once in a document, planning on adding support 
   to change the module for the tags
2. `Grid` - Enables explicit control of the griding method despite all elements 
   using `.grid()` instead of `.place` to add elements to the grid. Uses 
   `ColumnDefinition`s and `RowDefinitions` to control how these are done. 
   Uses custom attributes in the elements to control how they are placed. 
   See the example in `simple.xml`. Currently, resizing does not work nor is 
   alignment implemented.
3. `Button` - Ability to change text and add callbacks 
4. `TextBlock` - Resolves to a TKinter `Label`
5. `BaseElement` - Base class which all elements should derive from. Defines 
   the default constructor to manage attributes and children. All elements have 
   a function with signature `def backing_element_generator(self, parent: tkinter_xml.BaseElement) -> tkinter.Frame` 
   which is used to render the page contents recursively.

## Custom Attributes

These are in the form of `attribute_namespace.attribute_name` and represents an 
arbitrary attribute (not checked if it is in the default attribute dictionary) 
which will be handled by the parent of the tag (for example `Grid.Column` and 
`Grid.Row` is processed by the `Grid` element and should be ignored by all 
other elements).

## Tag Resolution

Tags must be in the namespace of the `BaseElement`-derived class otherwise the 
`eval` used to resolve the tag name will not be able to find the intended tag 
type.

## Reserved Attributes

There are two categories of reserved attributes: event handlers and 
variable-based attributes. These mainly operate around the use of the backing 
class to provide both data-access and data-reading.

### Event Handlers

Currently, event handlers are tested by comparing them to a set of attributes 
(currently only `Click` but this will likely be expanded and made custom 
per-element). Once the attribute has been identified as being an event handler, 
the attribute is resolved to the function on the parent page class using 
`getattr`.

### Variable-Based Attributes

`x_Name` Signifies that the element should be assigned to the variable specified
by the attribute on the page class. This employs `setattr` to make this
possible.

Plans to add binding (referenced-based values for elements such as `TextBlock`).

## Folder Structure

 - `tkinter_xml` - Contains the module for processing and converting the base
   xml into tkinter widgets
   - `elements` - Contains the pre-defined elements as above.
   - `constants.py` - Contains globally-required constants
   - `Page.py` - Contains file-parsing and tag resolution capabilities
 - `main.py` - The entry point of the program which uses `tkinter_xml`
 - `simple.xml` - An example xml file showcasing the current abilities of the
   parser