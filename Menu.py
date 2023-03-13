class Menu:
    name = ""
    title = ""
    back = ""
    sub = []
    function = ""

    def __init__(self, dict_menu=None):
        if dict_menu is not None:
            self.name = dict_menu["name"]
            self.title = dict_menu["title"]
            self.back = dict_menu["back"]
            self.sub = dict_menu["sub"]
            self.function = dict_menu["function"]

    def to_dict(self):
        return dict(
            {
                "name": self.name,
                "title": self.title,
                "back": self.back,
                "sub": self.sub,
                "function": self.function,
            }
        )
