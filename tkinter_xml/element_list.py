"""Global xml tag to class 'registry'"""

element_list = {
}

def register_element(name: str, ty: type):
    """Sets a given tag to refer to a given class"""

    element_list[name] = ty

def retrieve_element(name: str):
    """retrieves a given type from a tag name"""

    return element_list[name]