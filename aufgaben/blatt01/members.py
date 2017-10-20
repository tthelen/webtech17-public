# coding: utf-8
# Uni Osnabrück, Web-Technologien 2017/2018
# Übungsblatt 01, Aufgabe 1-3
#

# https://docs.python.org/3/library/json.html
import json


def read_json(fn):
    """Read a members-json file from the file identified by fn. Content is parsed but not validated."""
    pass


def print_html(fn, name, members):
    """Print HTML table to file 'fn'. Uses 'name' for heading and walks through 'members' structure."""
    pass


if __name__ == '__main__':  # Python jargon for main - only executed if script is used as top level script
    infile = "members.json"
    outfile = "members.html"
    data = read_json(infile)
    print_html(outfile, data["name"], data["members"])
    print("HTML table written to '{}'".format(outfile))
