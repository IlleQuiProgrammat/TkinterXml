import tkinter as TK

d = {
            "content": "Button",
            "font_size": 12,
            "font_family": "Segoe UI",
            "foreground": "black",
            "click": lambda s: print("Button clicked"),
    }

def generate_string_parser(key):
    value = d[key]
    if isinstance(value, bool):
        return "bool(value)"
    if isinstance(value, int):
        return "int(value)"
    else:
        return "!!! FILL IN MANUALLY !!!"

for key in d.keys():
    print(f"self._{key} = {d[key]}")

print("\n"*10)

for key in d.keys():
    print(f"""
    @property
    def {key}(self):
        return self._{key}
    
    @{key}.setter
    def {key}(self, value):
        to_set = value
        if isinstance(value, str):
            to_set = {generate_string_parser(key)}
        self._{key} = to_set
        if self.immediate_update:
            self.reload()
    """)