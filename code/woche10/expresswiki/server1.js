
// builtin libraries
const fs = require('fs');  // file system access (node.js builtin)

// http framework
const express = require('express');  // express js framework (installed via npm)

const cookieParser = require('cookie-parser'); // middleware for parsing cookies
const bodyParser = require('body-parser');  // middleware for parsing request bodys
const accesslog = require('access-log'); // logging middleware

// templating engine
const mustacheExpress = require('mustache-express');  // mustache as template engine for express (installed via npm)

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

function pagelist() {
    // use synchronous I/O to get page list - return list of strings
    return fs.readdirSync('./data');
}

// show wiki page
function show(req, res, next) {
      var page = req.params['page'] || 'main';
      var pages = pagelist();
      fs.readFile('data/'+page, 'utf8', function (err, data) {
          if (err) return next(err);  // pass to next handler which is the error handler
          res.render('show.mustache', { 'text': markup(data), 'pagename': page, 'pages': pages});
      });
}

// show wiki page for editing
function edit(req, res, next) {
    var page = req.params['page'] || 'main';
    var pages = pagelist();
    fs.readFile('data/' + page, 'utf8', function (err, data) {
        if (err) return next(err);
        res.render('edit.mustache', {'text': data, 'pagename': page, 'pages': pages});
    });
}

// receive post request, save data and redirect to show
function save(req, res, next) {
      var page = req.params['page'] || 'main';
      var data = req.body.wikitext;
      fs.writeFile('data/'+page, data, function (err, data) {
          if (err) return next(err);
          res.redirect('/show/'+page);
      });
}

// setup und start express engine
var app = express();

app.engine('mustache', mustacheExpress());
app.set('views', './templates');
app.set('view engine', 'mustache');

// bodyParser middleware parses request bodies
app.use(bodyParser.urlencoded({ extended: true })); // enables parsing application/x-www-form-urlencoded

// logging middleware
app.use(function (req,res, next) {
   accesslog(req,res);
   next();
});

// error handling
app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// serve static files from ./static as /static
app.use('/static', express.static('static'));

// configure routes
app.get('/', show);
app.get('/show', show);
app.get('/show/:page(\\w+)', show);
app.get('/edit', edit);
app.get('/edit/:page(\\w+)', edit);
app.post('/save/:page(\\w+)', save);

// run the wiki app
app.listen(8080, function () { console.log('Wiki app listening on http://localhost:8080/'); });