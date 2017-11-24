"""
webserver.py

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 2 (04/2015)
"""

import socket, re, os
from server.log import log


class StopProcessing(Exception):
    """
    Exception: Immediately stop processing and issue an error response.
    """

    def __init__(self, code, reason):
        """
        Immediately stop processing and issue an error response.

        :param code: Error status code
        :param reason: Text to display
        """
        self.code = code
        self.reason = reason

    def __str__(self):
        """
        Representation for informational purposes.
        :return: Displayable string with code and reason
        """
        return "[%d] %s" % (self.code, self.reason)


class App:
    """An app wraps web applications or reusable components for
       web applications such as serving static files, providing
       statistical information on the server.

       An app registers it routes with the server and provides
       callbacks for these routes.
       """

    def __init__(self, **kwargs):
        """
        Initialises an app.

        The App base class recognizes these keywords:

        prefix - add a prefix to all routes the app registers.
                 The prefix must not have a leading or trailing slash.
                 Example: prefix=static

        :param kwargs: Keyword arguments
        """
        kwargs.setdefault('prefix', '')  # default: no prefix
        self.prefix = kwargs['prefix']  # set prefix

    def add_route(self, partial_route, handler):
        """
        Prefixes a route and adds it to server.

        :param partial_route: Partial route to match (may include named regex groups)
        :param handler: Function/Method to be called if route matches
        :return: Result of server.add_route
        """

        if self.prefix and partial_route and not partial_route.startswith('/'):
            partial_route = '/' + partial_route  # ensure / after prefix if there is a partial route without /
        prefixed_route = "^/" + self.prefix + partial_route
        if not prefixed_route.endswith('$'):  # add end anchor if necessary
            prefixed_route += '$'
        return self.server.add_route(prefixed_route, handler)

    def register_routes(self):
        pass


class Request:
    """
    http request data.
    """

    def __init__(self):
        self.headers = {}
        self.method = None
        self.protocol = None
        self.resource = None
        self.path = None
        self.params = {}
        self.origin = None  # will be set from server

    def parse(self, conn):
        """Parses an http-Request and return a dictionary with process_request line values and headers."""
        self.headers = {}

        # read process_request line
        request_line = conn.readline().decode('utf-8').strip()
        log(1, "Request-Line: %s" % request_line)
        if not request_line:  # rfc says "server SHOULD ignore blank request lines"
            return None

        # parse process_request line
        try:
            self.method, self.resource, self.protocol = request_line.split(" ")
        except ValueError:
            raise StopProcessing(400, "Bad request-line: %s\n" % request_line)

        # parse resource to path and params
        # extract GET parameters
        from urllib.parse import urlparse, parse_qs # analyse urls and parse query strings
        requrl = urlparse(self.resource)
        self.path = requrl.path
        self.params.update(parse_qs(requrl.query))

        # read and parse Request-Headers
        while True:
            header_line = conn.readline().decode('utf-8').strip()
            if not header_line:
                break
            log(2, "Header-Line: " + header_line)
            (headerfield, headervalue) = header_line.split(":", 1)
            self.headers[headerfield.strip()] = headervalue.strip()

        # parse POST parameters
        log(1,"Methode %s" % self.method)
        if self.method == 'POST' or self.method == 'post':
            postbody = conn.read(int(self.headers['Content-Length'])).decode('utf-8')
            self.params.update(parse_qs(postbody))

        # all parameter values are lists
        # replace lists by the only element if there is only one
        for key in self.params:
            if len(self.params[key])==1:
                self.params[key] = self.params[key][0]

        return self.headers


class Response:
    """
    http response data
    """

    def __init__(self, conn):
        self.conn = conn  # the connection to write to
        self.code = None  # status code
        self.headers = {}  # all the response headers
        self.body = None  # response body

    def add_header(self, key, value):
        """
        Adds or overwrites a given key-value pair to the http Headers.

        :param key: http-Header
        :param value: it's value
        """
        self.headers[key] = value

    def set_content_type(self, content_type):
        """
        Sets or overwrite the response's content type.

        :param content_type:
        """
        self.headers['Content-Type'] = content_type

    def send(self, code=None, headers=None, body=""):

        if not headers:
            headers = {}

        def w(txt):
            """Decode as UTF-8 and write to client connection"""
            self.conn.write(bytes(txt, 'UTF-8'))

        # method parameters overwrite/add to instance variables
        if code:
            self.code = code
        if body:
            self.body = body
        if headers:
            self.headers.update(headers)

        # default values
        if not self.code:
            self.code = 200
        if 'Content-Type' not in self.headers:
            self.headers['Content-Type'] = "text/html; charset=UTF-8"

        from server.statuscodes import statuscode

        (phrase, explanation) = statuscode(self.code)
        w("HTTP/1.1 %d %s\n" % (self.code, phrase))
        log(1, "HTTP/1.1 %d %s (%s)\n" % (self.code, phrase, explanation))

        import datetime

        w("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S"))
        w("Connection: close\n")
        for key, value in self.headers.items():
            w("%s: %s\n" % (key, value))
        w("\n")  # extra leerzeile schliesst header ab

        if self.body:
            if isinstance(self.body, str):
                w(self.body)
            else:
                self.conn.write(self.body)

    def send_template(self, template, dictionary={}, code=None, headers=None):
        """
        Reads a template file, substitutes placeholders and sends it.

        :param template: Template file name
        :param dictionary: Keys and values for template placeholders
        :param code: The status code (default: 200)
        :param headers: Additional headers (default: None)
        :return:
        """
        body = self.apply_template(template, dictionary)
        self.send(code=code, headers=headers, body=body)

    def apply_template(self, template, dictionary):
        """Applies a template and returns a string.

        Templates are normale Python format strings, with one addition:

        Sub-Templates (partials) can be used with this syntax:

        {{path/to/template:var}}

        The templates identified by the given path is then filled
        using the dictionary in var. If var is a list (of dictionaries),
        the template is filled in for each element in the list and then
        concatenated.

        Examples:

        templates/wiki/show.html:
        ...
        {{templates/wiki/header.tmpl}}
        ...
        <ul>
        {{templates/wiki/pagelist_entry.html:pages}}
        <ul>
        ...

        templates/wiki/pagelist_entry.html:
        <li><a href="{url}">{name}</a></li>

        templates/wiki/header.tmpl:
        ...
        <h1>{title}</h1>
        ...

        Invoked as:
        apply_template('template/wiki/show.html', {'title': 'The wiki page',
                                                   'pages': [ {'url': '/show/seite1', 'name': 'Seite 1'},
                                                              {'url': '/show/seite2', 'name': 'Seite 2'}]})

        :param template: Template file name
        :param dictionary: Keys and values for template placeholders
        :return: string
        """
        try:
            with open(template, "r", encoding="utf-8") as f:
                templ = f.read()
                # Sub-Template syntax:
                # {{/path/to/template}}     - reuse same dictionary
                # {{/path/to/template:var}} - use single key from dictionary (may be a list, then application is iterated)
                #
                # some regex magic:
                # [\w.- ,/]+  matches paths and filenames (\w = [a-zA-Z0-9_] + other word characters üäöß...)
                # [^\d\W]\w*  matches Python identifier (first sign = no digit, no non-word character, then \w
                #
                # we will have tuples with three matches: 0=entire placeholder, 1=template path, 3=variable name
                #
                partials = re.findall(r"({{([\w.-/]+)(:([^\d\W]\w*))?}})", templ)
                for partial in partials:
                    print(partial)
                    if partial[2]:  # key given
                        subdict = dictionary[partial[3]]
                    else:  # no key given
                        subdict = dictionary
                    print(subdict)
                    if isinstance(subdict, list):  # we have a list: concat iterated application of subtemplate
                        sub = ""
                        for element in subdict:
                            sub += self.apply_template(partial[1], element)
                    else:
                        sub = self.apply_template(partial[1], subdict)
                    templ = templ.replace(partial[0], sub)
                return templ.format(**dictionary) # Substitute with dictionary values/keys
        except KeyError as e:
            raise StopProcessing(500, "Template Error: Key {} not given".format(e))
        except IOError:
            raise StopProcessing(500, "Unable to open template %s." % template)


    def send_redirect(self, url):
        self.send(302, {'Location': url})


class Webserver:
    """Implements a simple webserver.

    In this version it receives and parses requests
    but always returns the same static response.

    Usage:
    server = Webserver(post=8080)
    server.serve()
    """

    def __init__(self, port=8080):
        self.port = port
        self.apps = []  # registered apps (App classes)
        self.routes = []  # registered routes (regex, handler)
        self.request = None
        self.response = None

    def add_app(self, app):
        """
        Register an app.
        :param app: App class instance
        :return: nothin
        """
        app.server = self  # set app's server attribute
        app.register_routes()  # let app register its routes
        self.apps.append(app)  # fill list of apps

    def add_route(self, route, action):
        """
        Register a route for request processing.
        """
        self.routes.append((route, action))

    def serve(self):
        """
        Listen for http requests forever and trigger processing.
        """

        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.bind(('localhost', self.port))
            c.listen(1)
        except socket.error as msg:
            log(0, msg)
            return

        log(0, "Server running on http://{}:{} .".format('localhost', self.port))

        while 1:
            csock, caddr = c.accept()
            conn = csock.makefile(mode='rwb', buffering=1)
            self.request = Request()
            self.response = Response(conn)

            if self.request.parse(conn):
                self.request.origin = caddr[0]
                log(2, "Request: %s\n" % self.request)
                try:
                    # processing (check registered routes for actions)
                    processed = False
                    for route in self.routes:
                        log(2, "Matche %s gegen %s" % (route[0], self.request.path))
                        match = re.match(route[0], self.request.path)
                        if match:
                            log(2, "Route %s matcht Request %s" % (route[0], self.request.path))
                            route[1](self.request, self.response, match)
                            processed = True
                            break
                    if not processed:
                        raise StopProcessing(404, "No matching route.")

                except StopProcessing as spe:
                    self.response.send(code=spe.code, body=spe.reason)

            conn.close()
            csock.close()
