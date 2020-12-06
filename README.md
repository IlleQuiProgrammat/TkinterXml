# TkinterXml

A Program designed to parse the tree of a XML document and render the result 
using tkinter

## Running

```bash
python3 -m venv venv

# linux and macos
source .\venv\bin\activate

# windows powershell
.\venv\Scipts\Activate.ps1
# windows cmd
.\venv\Scripts\activate.bat

python3 -m pip install -r ./requirements.txt

# Documentation:
# linux
cd ./docs; make html; xdg-open ./_build/html/index.html; cd ..
# macos
cd ./docs; make html; open ./_build/html/index.html; cd ..
# windows
cd .\docs; .\make.bat html; explorer.exe .\_build\html\index.html; cd ..

# Quotes App:
python3 ./quotes.py
```

# Brief Overview Documentation

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
   a function with signature `def backing_element_generator(self, parent) -> tkinter.Frame` 
   which is used to render the page contents recursively.

## Custom Attributes

These are in the form of `attribute_namespace.attribute_name` and represents an 
arbitrary attribute (not checked if it is a valid property on the derived class) 
which will be handled by the parent of the tag (for example `Grid.column` and 
`Grid.row` is processed by the `Grid` element and should be ignored by all 
other elements).

## Tag Resolution

Tags must be registered with `tkinter_xml.element_list.register_element(name, class)`
so that they can be resolved.

## Event Handlers

Event handlers act like any other attribute but should be parsed with the following snippet:

```py
if isinstance(value, str):
    to_set = getattr(self.parent_page, value)
```

## Reserved Attributes

### Element Variables on Page Class

The attribute `x_Name` signifies that the element should be assigned to the variable specified by the attribute on the page class. This users `setattr` to set the element accordingly. It sets the `BaseElement`-derived class rather than the tkinter object.

Plans to add binding (referenced-based values for elements such as `TextBlock`).

> Note: this would probably require setting up some sort of observable class which stores the functions which should be called when the value changes

## Changing element properties

Simply run `my_obj.<property_to_change> = <new_value>` and then `my_obj.reload()` unless you have auto-update enabled.

## Folder Structure
 - `helpers` - Currently contains some code-generation helpers
 - `tkinter_xml` - Contains the module for processing and converting the base
   xml into tkinter widgets
   - `elements` - Contains the pre-defined elements as above.
   - `Page.py` - Contains file-parsing and tag resolution capabilities
 - `main.py` - The entry point of the program which uses `tkinter_xml`
 - `simple.xml` - An example xml file showcasing the current abilities of the
   parser
