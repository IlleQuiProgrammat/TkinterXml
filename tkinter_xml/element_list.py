element_list = {
}

def register_element(name, ty):
    element_list[name] = ty

def retrieve_element(name):
    return element_list[name]