from string import Template


class Templating:
    """Use python string.format for templating."""
    @classmethod
    def render(cls, path, filename, dictionary):
        with open(path+'/'+filename, "r", encoding="utf-8") as file:
            templ = file.read()
            return templ.format(**dictionary)