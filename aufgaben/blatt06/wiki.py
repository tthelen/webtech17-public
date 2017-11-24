"""
wiki.py
A very very simple Wiki

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain / CC0
@status: completed
@version: 5 (11/2017)
"""

from server import webserver
from server.apps.static import StaticApp
from server.middlewares.session import SessionMiddleware
import re
import os


class NoSuchPageError(Exception):
    """Raise if try to access non existant wiki page."""
    pass


class WikiApp(webserver.App):
    """
    Webanwendung zum kollaborativen Schreiben (wiki).

    Diese sehr einfache Anwendung demonstriert ein simples Wiki.
    """

    def register_routes(self):
        self.add_route("", self.show)
        self.add_route("show(/(?P<pagename>\w+))?", self.show)
        self.add_route("edit/(?P<pagename>\w+)", self.edit)
        self.add_route("save/(?P<pagename>\w+)", self.save)
        self.add_route("create", self.create)

    def read_page(self, pagename):
        """Read wiki page from data directory or raise NoSuchPageError."""

        try:
            with open("data/"+pagename, "r", encoding="utf-8", newline='') as f:
                x = f.read()
                return x
        except IOError:
            raise NoSuchPageError

    def pages(self):
        """Return a html string for displaying page information."""
        pages = os.listdir("data")
        return ''.join(
            ["<li class='pure-menu-item'><a href='/show/{page}' class='pure-menu-link'>{page}</a></li>".format(page=x)
             for x in pages])

    def markup(self, text):
        """Substitute wiki markup in text with html."""

        text = re.sub(r"<", r"&lt;", text)
        # substitute links: [[pagename]] -> <a href="/show/pagename">pagename</a>
        text = re.sub(r"\[\[([a-zA-Z0-9]+)\]\]", r"<a href='/show/\1'>\1</a>", text)
        # substitute headlines: !bang -> <h1>bang</h1>
        text = re.sub(r"^!(.*)$", r"<h1>\1</h1>", text, 0, re.MULTILINE)
        # replace two ends of line with <p>
        text = re.sub(r"\r?\n\r?\n", r"<p>", text)
        # replace one end of line with <br>
        text = re.sub(r"\r?\n\r?\n", r"<br>", text)
        return text

    def send_error(self, response, error, text, pagename='main', pagetitle='Error'):
        """Fill the error template and send it."""
        response.send_template("wikierror.html",
                               {'error': 'No pagename given.',
                                'text': 'save action needs pagename',
                                'pages': self.pages(),
                                'pagename': 'main',
                                'pagetitle': 'Error: invalid pagename'
                                }, code=500)

    def show(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        try:
            pagename = pathmatch.group('pagename') or "main"
        except IndexError:
            pagename = "main"  # default pagename

        try:
            text = self.read_page(pagename)
        except NoSuchPageError:
            # redirect to edit view if page does not exist
            response.send_redirect("/edit/" + pagename)
            return

        # show page
        response.send_template('show.html',
                                   {'text': self.markup(text),
                                    'pagename': pagename,
                                    'pagetitle': 'Show Wiki Page',
                                    'pages': self.pages()})

    def edit(self, request, response, pathmatch=None):
        """Display wiki page for editing."""

        try:
            pagename = pathmatch.group('pagename') or "main"
        except IndexError:
            pagename = "main"

        try:
            text = self.read_page(pagename)
        except NoSuchPageError:
            # use default text if page does not yet exist
            text = "This page is still empty. Fill it."

        # fill template and show
        response.send_template('edit.html',
                                   {'text': text,
                                    'pages': self.pages(),
                                    'pagetitle': 'Edit wiki page',
                                    'pagename': pagename})

    def create(self, request, response, pathmatch=None):
        """Check name and show error message or edit view."""

        try:
            pagename = request.params['pagename']
        except KeyError:
            return self.send_error(response,'No pagename given.', 'save action needs pagename')

        if not re.match(r"^[a-zA-Z0-9_-]+$", pagename):
            return self.send_error(response, 'Invalid pagename',
                                   'Invalid pagename: {}. Use a-z, A-Z, 0-9 and _ or - only.'.format(pagename))
        else:
            response.send_redirect("/edit/"+pagename)

    def save(self, request, response, pathmatch=None):
        """Evaluate request and construct response."""

        try:
            pagename = pathmatch.group('pagename')
        except IndexError:
            # no pagename given: error
            return self.send_error(response, 'No pagename given.', 'save action needs pagename')

        try:
            wikitext = request.params['wikitext']
        except KeyError:
            # no text given: error
            return self.send_error(response, 'No text given.', 'save action needs text.')

        f = open("data/" + pagename, "w", encoding='utf-8', newline='')
        f.write(wikitext)
        f.close()

        response.send_redirect("/show/"+pagename)


if __name__ == '__main__':
    s = webserver.Webserver()
    s.set_templating("python_format")  # use good old string.format for templating (like we used to in the past weeks)
    s.set_templating_path("templates/wiki")  # where are the templates?
    s.add_app(WikiApp())
    s.add_app(StaticApp(prefix='static', path='static'))
    s.add_middleware(SessionMiddleware())  # let's have sessions (not really needed for this version but if you add auth...)
    s.serve()
