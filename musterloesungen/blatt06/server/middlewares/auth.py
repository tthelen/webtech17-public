from server.webserver import Middleware, AlreadyProcessed
import json
import re


class AuthMiddleware(Middleware):
    """Add a session attribute to request.

    The auth middleware provides to methods to be called from apps:

    check()  - returns None is not authenticated or the current username

    do()  - Returns the name of the authenticated user. If current user is
            not authenticated, the middleware sends a login template and
            checks it. do() never returns for an unauthenticated user.
    """

    def __init__(self, template=None):
        self.template = template
        self.username = None  # None means: not authenticated
        self.users = {}  # will hold dictionary with usernames/passwords
        self.request = None
        self.response = None
        self.read_users()  # read in users
        super().__init__()

    def process_request(self, request, response):
        """Check if auth info is in session."""
        self.request = request
        self.response = response
        request.auth = self  # attach myself to request object
        self.username = self.request.session.get('username', None)

    def check(self):
        """Return username if user is authenticated, else false."""
        return self.username

    def do(self, message=None, additional_template_params=None):
        """Check if user is authenticated and return username. If not, display login form or process login form.

        'do' only returns if user could be authenticated.

        :message (string)  A message to be displayed.
        :additional_template_params (dict)  Additional, app specific parameters for the template."""

        # if we have to display a login form, we need to reconstruct the original query afterwards
        # for to do this, we need (nearly) all the request parameters as hidden input fields in the form
        # Plus: If text contains quotes, we need to mask them as &quot;
        for x in self.request.params.items():
            print(x)
        template_params = {'username': '',
                           'password': '',
                           'message': message,
                           'params': [{'key': x[0], 'value': re.sub('"', '&quot;', x[1])}
                                      for x in self.request.params.items() if x[0] not in ['username', 'password', '__login']]}

        # the app can set additional template parameters like side bar fillings etc.
        if additional_template_params:
            template_params.update(additional_template_params)

        # magic parameter __login: check given credentials
        if '__login' in self.request.params:
            login_username = self.request.params.get('username','')
            login_password = self.request.params.get('password','')
            if login_username in self.users and self.users[login_username] == login_password:
                self.username = login_username  # hurray, we are authenticated!
                self.request.session['username'] = self.username
            else:
                self.username = None
                template_params.update({'username': login_username, 'password': login_password})
                self.response.send_template(self.template, template_params)
                raise AlreadyProcessed()  # skip any further app route processing
        elif self.username:
            return self.username  # return to app
        else:
            self.response.send_template(self.template, template_params)
            raise AlreadyProcessed()    # skip any further app route processing

    def logout(self):
        """Logout by setting username to None in session."""
        self.username = None
        self.request.session['username'] = None
        # processResponse handler for session will save this value

    def read_users(self):
        """Read json file with user credentials."""
        try:
            with open("users.json") as f:
                self.users = json.load(f)
        except (IOError, json.JSONDecodeError):
            print("Could not load users from users.json!")
            exit(1)