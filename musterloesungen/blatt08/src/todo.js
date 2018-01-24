/*
 todo.js
 Tobias Thelen, 2017-18
 Public Domain
*/

import _ from 'lodash';  // lodash for convienience functions for arrays, objects, ...
import $ from 'jquery';  // jQuery for easier DOM manipulation
import xssFilter from 'xssfilter';  // xssfilter
import todolist from './todomodel'; // import model

// Notice: You need a rule for css files to use the style-loader and the css-loader
import 'purecss/build/pure-min.css';  // tell webpack to include the css.
import './test.css';

$(function () {

    // format a todo item
    // :param item (TodoList object) The todo list item
    // :param idx (int) its index (used to identify object for marking or deleting)
    function entry(item, idx) {
        var ret = "";
        ret += "<p>";

        // the checkbox (class 'checker')
        ret += '<input type="checkbox" class="checker" ';
        if (item.done) {  // make the checkbox checked if item is marked as done
            ret += "checked ";
        }
        // put index in data attribute
        ret += 'data-idx="' + idx + '"> ';

        // the item description
        if (item.done) {  // grey and strike-through if done
            ret += "<span style='color:grey; text-decoration: line-through;'>";
        } else {
            ret += "<span>";
        }
        ret += item.text + '</span>';

        // the delete 'button' (red cross)
        // css-class: 'remover'
        // index given as data-idx attribute
        ret += " <a href='#' style='color:red; text-decoration:none;' class='remover' data-idx='"+idx+"'>X</a></p>";
        return ret;
    }

    // update the todo list
    function update() {
        $('#thelist').html('');
        _.each(todolist.list, function (item, idx) {
            $('#thelist').append(entry(item, idx));
        });
    }

    // add a new item after filtering it for xss
    // :param val (string) Text of item to add
    function add(val) {
        var xssf = new xssFilter();
        var filtered = xssf.filter(val);
        if (filtered) {  // only add if it has text (after filtering)
            todolist.add(filtered);
            update();
        }
    }

    // handle new todos
    $('#theinputform').submit( function (event) {
       add($('#theinput').val());
       $('#theinput').val('');  // clear the input field
       event.preventDefault();  // don't send the form!
    });

    // handle "done/undone" clicks
    $(document).on('change', '.checker', function () {
        todolist.mark($(this).data('idx'), this.checked);
        update();
    });

    // handle "delete" clicks
    $(document).on('click', '.remover', function () {
        todolist.remove($(this).data('idx'));
        $(this).parent().fadeOut().slideUp(update);  // fade out element and update list view
    });

    // initialize with saved entries or default entries, then update list view
    todolist.init(update);
});
