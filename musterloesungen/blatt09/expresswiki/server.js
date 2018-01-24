/*
the webtech wiki for node.js/express

tobias thelen, 2017-2018
public domain
 */

// builtin and general libraries
const fs = require('fs');  // file system access (node.js builtin)
const _ = require('lodash');  // utility functions

// http framework
const express = require('express');  // express js framework (installed via npm)

// common express middlewares
const cookieParser = require('cookie-parser'); // middleware for parsing cookies
const bodyParser = require('body-parser');  // middleware for parsing request bodys
const accesslog = require('access-log'); // logging middleware

// authentication middleware (passport)
const expressSession = require('express-session');  // express session support
const passport = require('passport'); // authentication middleware
const Strategy = require('passport-local').Strategy;  // local authentication strategy for passport
const ensureLoggedIn = require('connect-ensure-login').ensureLoggedIn;  // redirect to login for actions that need auth

// templating engine
const mustacheExpress = require('mustache-express');  // mustache as template engine for express (installed via npm)


// state variables
var watchers = {};  // all watchers, organized by pagename (object with pagenames as properties, list of socket as values)
var editors = {};   // all edited pages, organized by pagename (object with pagenames as properties, boolean as values)

// wiki functions
function markup(text) {

    // substitute < by &lt;
    text = text.replace(/</g, "&lt;");
    // substitute links: [[pagename]] -> <a href="/show/pagename">pagename</a>
    text = text.replace(/\[\[([a-zA-Z0-9]+)\]\]/g, "<a href='/show/$1'>$1</a>");
    // substitute headlines: !bang -> <h1>bang</h1>
    text = text.replace(/^!(.*)$/gm, "<h1>$1</h1>");
    // replace two ends of line with <p>
    text = text.replace(/\r?\n\r?\n/gm, "<p>");
    // replace one end of line with <br>
    text = text.replace(/\r?\n\r?\n/gm, "<br>");

    return text
}

function pagelist(callback) {
    // use synchronous I/O to get page list - return list of strings
    return fs.readdirSync('./data');
}
// show wiki page
function show(req, res, next) {
      var page = req.params['page'] || 'main';
      var pages = pagelist();
      var username = req.user;
      fs.readFile('data/'+page, 'utf8', function (err, data) {
          if (err) return next(err);  // pass to next handler which is the error handler
          res.render('show.mustache', { 'text': markup(data), 'pagename': page, 'pages': pages, 'username': username });
      });
}

// show wiki page for editing
function edit(req, res, next) {
      var page = req.params['page'] || 'main';
      var pages = pagelist();

      if (editors[page]) { // page is currently edited. Show error message.
        return res.render('wikierror.mustache', {'pagename': page, 'pages': pages,
            'error':'Page is currently being edited.',
            'text':'Someone else is editing this page right now. Return to show to see them in action.'});
      }

      if (req.session.wikitext) {  // perhaps we have a saved text in the session to survive login
          req.session.wikitext = undefined;
          return res.render('edit.mustache', { 'text': req.session.wikitext, 'pagename': page, 'pages': pages });
      }
      fs.readFile('data/'+page, 'utf8', function (err, data) {
          if (err) data='This page is still empty. Fill it.';
          res.render('edit.mustache', { 'text': data, 'pagename': page, 'pages': pages });
      });
}

// show login page
function loginview(req, res, next) {
      var page = req.params['page'] || 'main';
      var pages = pagelist();
      res.render('login.mustache', { 'pagename': page, 'pages': pages });
}


// receive post request, save data and redirect to show
function save(req, res, next) {
      var page = req.params['page'] || 'main';
      var data = req.body.wikitext;
      req.session.wikitext = undefined;
      fs.writeFile('data/'+page, data, function (err, data) {
          if (err) return next(err);
          res.redirect('/show/'+page);
      });
}

function savewikitext(req, res, next) {
      req.session.wikitext = req.body.wikitext;
      next();
}

// check if a page to be created is well formed and still available
// Error handler will be called if pagename is empty or not wellformed or already exists
// Otherwise, user will be redirected to edit new page
function create(req, res, next) {
    var pagename = req.query.pagename;
    console.log(req.params);
    if (!pagename) return next("Error: No pagename given.");
    if (!(pagename.match(/^\w+$/))) return next("Error: Page name "+pagename+" contains forbidden characters. Only use letters and numbers, no spaces.");
    if (fs.existsSync('data/'+pagename)) return next("Page "+pagename+" already exists.");
    res.redirect('/edit/'+pagename);
}

// setup und start express engine
var app = express();
var server = require('http').createServer(app)
var io = require('socket.io').listen(server)

app.engine('mustache', mustacheExpress());
app.set('views', './templates');
app.set('view engine', 'mustache');

// Middlewares
//
//

// bodyParser middleware parses request bodies
app.use(bodyParser.urlencoded({ extended: true })); // enables parsing application/x-www-form-urlencoded

// logging middleware
app.use(function (req,res, next) {
   accesslog(req,res);
   next();
});

// serve static files from ./static as /static
app.use('/static', express.static('static'));
app.use(require('cookie-parser')());

// configure authorization
app.use(require('express-session')({ secret: '0815secret', resave: false, saveUninitialized: false }));

passport.use(new Strategy(
  function(username, password, cb) {
    if (username=='admin' && password=='admin') {
        return cb(null, 'admin');
    } else {
        return cb(null, false);
    }
  }));

// map session representation to user object (we use the same string in both cases)
passport.serializeUser(function(user, cb) { cb(null, user); });
passport.deserializeUser(function(id, cb) { cb(null, id); });

// Initialize Passport and restore authentication state, if any, from the session.
app.use(passport.initialize());
app.use(passport.session());


// configure routes
app.get('/', show);
app.get('/show', show);
app.get('/show/:page(\\w+)', show);
app.get('/edit', ensureLoggedIn('/login'), edit);
app.get('/edit/:page(\\w+)', ensureLoggedIn('/login'), edit);
app.post('/save/:page(\\w+)', savewikitext, ensureLoggedIn('/login'), save);
app.get('/save/:page(\\w+)', function (req, res) { res.redirect('/edit/'+req.params['page']); });
app.get('/create', ensureLoggedIn('/login'), create);

// logging in an out
app.get('/login', loginview);
app.post('/login', passport.authenticate('local', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));
app.get('/logout',
  function(req, res){
    req.logout();
    res.redirect('/');
});

// error handling (needs to be defined AFTER the routes)
app.use(function(err, req, res, next) {
    res.render('wikierror.mustache', {'error': 'Something went wrong...', 'text':err, 'pages': pagelist(), 'pagename':'Error'})
});


// Websocket handling
// someone connects
io.sockets.on('connection', function (socket) {
    var mode;  // show or edit?
    var page;  // save page for this socket
	socket.on('edit', function (data) {  // client starts editing
		page = data.page;
        mode = 'edit';
        editors[page] = true; // mark page as currently edited
        console.log("Socket #"+socket.id+" connected as an editor on page "+page);
	});
	socket.on('show', function (data) {  // client stats watching
	    page = data.page;
	    mode = 'show';
	    if (watchers.hasOwnProperty(page)) {
	        watchers[page].push(socket); // add client to list of watchers
        } else {
	        watchers[page]=[socket]; // add client to list of watchers
        }
        console.log("Socket #"+socket.id+" connected as a watcher on page "+page);
    });
	socket.on('input', function (data) {  // editor changes text
        console.log("Socket #"+socket.id+" wrote >>"+data.text+"<< on  "+page);
        console.log("Watcher stack is:");
        console.log(watchers);
	    if (watchers.hasOwnProperty(data.page)) { // if there are watchers (list might be empty)
	        _.each(watchers[data.page], function (w) {  // send changed text to all watchers
                console.log("Emit input to "+w.id);
	            w.emit('input', markup(data.text));
            });
        }
    });
	socket.on('disconnect', function () {  // client goes away
        if (mode == 'edit') editors[page] = false;  // mark page as not currently edited
        if (mode == 'show') _.pull(watchers[page], socket); // remove client from watcher list
	});
});

// run the wiki app
server.listen(8080, function () { console.log('Wiki app listening on http://localhost:8080/'); });
