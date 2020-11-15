import tkinter as TK

d = {
    "active_background": "gray",
    "active_foreground": "black",
    "anchor": TK.CENTER,
    "background": "gray",
    "bitmap": "",
    "border_width": 1,
    "compound": TK.NONE,
    "cursor": "hand1",
    "default": TK.DISABLED,
    "disabled_foreground": "gray",
    "height": 0,
    "highlight_background": "",
    "highlight_color": "blue",
    "highlight_thickness": 2,
    "image": "",
    "justify": TK.CENTER,
    "over_relief": TK.FLAT,
    "padding": (10,10),
    "relief": TK.FLAT,
    "repeat_delay": -1,
    "repeat_interval": -1,
    "state": TK.NORMAL,
    "take_focus": "",
    "underline": -1,
    "width": 0,
    "wrap_length": 0,
    "text": "Button",
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

print("\n"*10)

for key in d.keys():
    print(f"{key.replace('_', '')}=self.{key}")