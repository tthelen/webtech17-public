
from server.webserver import Webserver, App
from server.apps.static import StaticApp


class IndexApp(App):
    """Create a nice index page for the server and list all apps."""

    def __init__(self, **kwargs):
        """Initialize. Extra parameter: servername."""

        if 'servername' in kwargs:
            self.servername = kwargs['servername']
        else:
            self.servername = "The Server."
        super().__init__(**kwargs)

    def register_routes(self):
        """Register the only route on '' and make it default."""
        self.add_route('', self.index, default_entry=True)

    def index(self, request, response, pathmatch=None):
        """Create index page (text/html)"""

        print(self.server.apps)
        body="""
        <html>
          <head>
            <title>{}</title>
          </head>
        <body>
          <h1>{}</h1>
          <ul>
            {}
          </ul>
        </body>
        </html>""".format(self.servername, self.servername,
                          "".join(["<li>{} - <a href='{}'>{}</a></li>".format(a.name, a.default_entry, a.default_entry) for a in self.server.apps]))
        response.set_content_type("text/html")
        response.send(body=body)


class FortyTwoApp(App):
    """A very wise simple App."""
    def register_routes(self):
        self.add_route("", self.theanswer)

    def theanswer(self, request, response, pathmatch):
        response.send(200, body="<html><body><h1>42</h1></body></html>")


if __name__ == '__main__':
    s = Webserver()

    # Static app for static folder
    static = StaticApp(prefix='static', path='static', name='Statischer Dateibereich')
    static.default_entry="/static/"
    s.add_app(static)

    # Flappy Bird clone via StaticApp
    floppy = StaticApp(prefix='floppy', path='3rdparty/floppybird', name='Floppy Bird (js game)')
    floppy.default_entry="/floppy/index.html"
    s.add_app(floppy)

    # 2048 game via StaticApp
    game2048 = StaticApp(prefix='2048', path='3rdparty/2048', name='2048 (js game)')
    game2048.default_entry="/2048/index.html"
    s.add_app(game2048)

    # Some great app
    s.add_app(FortyTwoApp(prefix='42'))

    # The Index app
    s.add_app(IndexApp(prefix=''))

    s.serve()
