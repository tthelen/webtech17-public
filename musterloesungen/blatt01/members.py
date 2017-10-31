# coding: utf-8
# Uni Osnabrück, Web-Technologien 2017
# Übungsblatt 0, Aufgabe 1
#
# Aufgabenstellung:
#
# Erstellen Sie eine JSON-Datei `members.json`, die wie folgt strukturiert ist:
#
#  Auf oberster Ebene gibt es ein Dictionary mit zwei Schlüsseln (Keys):
#   1. 'name': Der Team-Name (String)
#   2. 'members': Eine Liste von Mitgliedern.
#                 Jedes Mitglied wird durch ein Dictionary repräsentiert,
#                 das folgende Schlüssel enthält:
#                 'firstname' - Der Vorname (string)
#                 'lastname' - Der Nachname (string)
#                 'githubname' - Der Github-Benutzername (string)
#                 'studipname' - Der Stud.IP-Benutzername (string)
#


# https://docs.python.org/3/library/json.html
import json


class WebTechError(Exception):
    """Just an identifiable Exception class with no additional funcitionality."""
    pass


def read_json(fn):
    """Read a members-json file from the file identified by fn. Content is parsed but not validated."""
    try:
        # when dealing with files, always use context managers (a.k.a. 'with' statements)
        # why? read this: https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/
        with open(fn, "r") as f:
            return json.load(f)
    except IOError as e:  # Aufgabe 3: File does not exist or is not readable
        raise WebTechError("Unable to open file {} ({})".format(fn, e))
    except json.JSONDecodeError as e:  # Aufgabe 3: File content cannot be parsed as json
        raise WebTechError("Invalid json data in file {} ({})".format(fn, e))


def write_html(fn, name, members):
    """Print HTML table to file 'fn'. Uses 'name' for heading and walks through 'members' structure."""
    try:
        with open(fn, "w") as f:
            f.write("<h1>{}</h1>\n".format(name))
            f.write("<table>\n")
            f.write("  <tr><td>Vorname</td><td>Nachname</td><td>Github</td><td>Stud.IP</td></tr>\n")
            try:
                for row in members:
                    f.write("  <tr>")
                    for key in ["firstname", "lastname", "githubname", "studipname"]:
                        try:
                            f.write("<td>{}</td>".format(row[key]))
                        except KeyError:  # Aufgabe 3: handle inexistant key in a single row
                            raise WebTechError("Malformed json data, key '{}' does not exist in row {}.".format(key, row))
                    f.write("</tr>\n")
            except TypeError as e:  # Aufgabe 3: List or object expected from Json data but something else found
                raise WebTechError("Invalid type in json data ({})".format(e))
            f.write("</table>\n")
    except IOError:  # Aufgabe 3: impossible to open file for writing
        raise WebTechError("Unable to open file {} for writing ({})".format(fn, e))


if __name__ == '__main__':  # Python jargon for main - only executed if script is used as top level script
    infile = "members.json"
    outfile = "members.html"
    try:
        data = read_json(infile)
        write_html(outfile, data["name"], data["members"])
    except WebTechError as e:  # something expected went wrong
        print("Error!")
        print(e)
    else:  # nothing went wrong
        print("HTML table written to '{}'".format(outfile))

        # Addition:
        # funny fancy stuff to display the HTML directly
        # the standard library module 'webbrowser' provides an
        # interface to start a webbrowser

        import webbrowser
        import os  # get current path

        # os.getcwd() returns the absolute path of current working directory
        # os.path.join(path, paths..) joins path parts in the correct way for current operating system
        url = "file://{}".format(os.path.join(os.getcwd(), outfile))
        webbrowser.open_new_tab(url)