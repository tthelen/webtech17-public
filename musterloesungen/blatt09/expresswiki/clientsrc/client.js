import $ from 'jquery';

import io from 'socket.io-client';  // the socket.io client

import 'purecss/build/pure-min.css';  // tell webpack to include the css.
import 'purecss/build/grids-responsive-min.css';
import './wiki.css';


$(document).ready(function(){
	var socket = null;    // the socket.io socket
	var mode = null;   	  // show or edit or nothing (like error)
	var pagename = null;  // page currently shown or edited

	// parse current url to find out what we're doing
	var url = window.location.href;
	var match = url.match(/(show|edit)\/(\w+)/);
	if (match) {
		mode = match[1];
		pagename = match[2];
	}

	if (mode=='edit') {  // when editing we want to send all changes to server
		socket = io.connect();
		socket.emit('edit', { page: pagename });
		$('#wikiedit').on("input", function (event) {
            // changes to textarea content fire input event
            // then we emit an input message to server to be distributed to all watchers
            // payload is object with pagename and current text
			socket.emit('input', { page: pagename, text: $('#wikiedit').val() });
		});
	}

	if (mode=='show') {  // when showing we want to receive changes from server
		socket = io.connect();
		console.log("I show!");
		socket.emit('show', { page: pagename });
		socket.on('input', function (textdata) {
            // if we receive an input message from the server, we update the text.
            // the payload is just an html string (markup rules already applied)
			$('#wikitext').html(textdata);
		});
	}
});