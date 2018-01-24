'''
Created on 10.05.2013

@author: Tobias
'''

from server.webserver import Webserver, App, StopProcessing
from server.apps.static import StaticApp
from server.apps.usermanagement import UsermanagementApp
from server.apps.static import StaticApp
from server.middlewares.session import SessionMiddleware
from server.log import log
import server.usermodel

import sqlite3 as sqlite
import os
from urllib.parse import quote, unquote
import re


class MiniTwitterApp(App):
    """Create and display status messages"""

    def __init__(self, datadir='data', db_connection=None):
        self.datadir = datadir
        self.db_connection = db_connection
        super().__init__()

    def register_routes(self):
        self.server.add_route(r"/?$", self.show)
        self.server.add_route(r"/logout$", self.logout)
        self.server.add_route(r"/login$", self.login)
        self.server.add_route(r"/tweets$", self.tweets)
        self.server.add_route(r"/save$", self.save)

    def show(self, request, response, pathmatch):
        """Process all requests. Dispatch POST to save method. Show tweets on GET requests."""

        if request.method.lower() == 'post':
            return self.save(request, response, pathmatch)

        try:
            message = request.params['message']
        except KeyError:
            message = ""

        try:
            user = request.session['user']
        except (AttributeError, KeyError):
            user = server.usermodel.AnonymousUser()

        d = {'message': message, 'user': user }

        response.send_template('minitwitter.tmpl', d)

    def tweets(self, request, response, pathmatch):
        import time
        time.sleep(2);
        m = []  # list of tweets
        try:
            f = open(self.datadir+'/minitwitter.data','r', encoding='utf-8')
            lines = f.readlines()
            f.close()
        except IOError:
            # no tweets, yet
            lines=[]

        for line in lines:  # parse all lines and build array of tweets with dates
            try:
                splitline = line.strip().split("#")
                tweet = splitline[0]
                author = splitline[1]
                date = splitline[2]
                tweet = re.sub(r"&#59", ";", tweet)  # TT: Hack: replace ; by &#59 and reconvert after reading
            except (ValueError, KeyError, IndexError):
                # ignore corrupt lines
                continue
            m.append({'date': date, 'tweet': tweet, 'author': author})
        if not m:
            m.append({'date': 'No news', 'tweet': 'Create some.', 'author':'The Minitwitter'})
        m.reverse()

        d = {'tweets': m }

        response.send_template('tweets.tmpl', d)

    def save(self, request, response, pathmatch):
        """Process post request to save new tweet."""

        if 'user' not in request.session:
            raise StopProcessing(400, "You need to be logged in.")

        import datetime
        now = datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")
        try:
            status = request.params['status']
        except KeyError:
            raise StopProcessing(500, "No status given.")
        try:
            f=open(self.datadir+'/minitwitter.data','a', encoding='utf-8')
            status = re.sub(r";", "&#59", status)  # TT: Hack: replace ; by &#59 and reconvert after reading
            f.write(status + "#"+ request.session['user'].fullname + "#" + now + "\n")
            f.close()
        except IOError:
            raise StopProcessing(500, "Unable to connect to data file.")
        
        response.send_redirect("/?message={}".format(quote("Great! Now the world knows.")))

    def logout(self, request, response, pathmatch):
        if request.session:
            request.session.destroy()
        response.send_redirect("/?message=Successfully logged out.")

    def login(self, request, response, pathmatch):
        if 'user' in request.session:  # already logged in
            return response.send_redirect("/")
        if '_username' in request.params and '_password' in request.params:
            users = server.usermodel.Users(self.db_connection)
            user = users.login(request.params['_username'], request.params['_password'])
            if user:
                request.session['user'] = user  # save user to session
                return response.send_redirect("/?message=Successfully logged in as <i>{}</i>.".format(request.params['_username']))
            else:
                return response.send_template('login.tmpl',{'message':'Wrong username or password. Try again.'})
        # send login form
        return response.send_template('login.tmpl',{})


if __name__ == '__main__':

    db = sqlite.connect('minitwitter.sqlite')
    db.row_factory = sqlite.Row

    s = Webserver()
    s.set_templating("pystache")
    s.set_templating_path("templates.mustache")

    s.add_middleware(SessionMiddleware())

    s.add_app(UsermanagementApp(db_connection=db))
    s.add_app(StaticApp(prefix='static', path='static'))

    s.add_app(MiniTwitterApp('data', db_connection=db))

    log(0, "Server running.")
    s.serve()
