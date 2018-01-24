// todomodel.js
import _ from 'lodash';
import localforage from 'localforage';

// An object holding the todo list and its methods
// Items are identified by their index in the todo list
// These indices change after removing an element from the list!
export default {
    list: [],  // a list of TodoItems
    add: function (text) {  // add a new todo item
        this.list.push(new TodoItem(text));
        this.store();
    },
    remove: function(idx) {  // remove a todo item
        // _.remove takes a function with (value, index) that returns true if item is to be removed
        _.remove(this.list, function (val, i) { return i == idx; });
        this.store();
    },
    mark: function (idx, done) {  // mark a todo item as done
        this.list[idx].done = done;
        this.store();
    },
    store: function () {
        localforage.setItem('todolist', this.list);
    },
    init: function (callback) {
        var that = this;  // save "this" for use in different context

        localforage.getItem('todolist', function (err, list) {
            // callback: item retrieved
            if (list) {
                that.list = list;
            } else {
                // no entries yet: use default entry
                that.add("Mark this item as done.");
                that.add("Add more items.");
            }
            callback();  // call action after completion
        });

    }
}

// a TodoItem model with just two properties:
// - text (string): The description
// - done (boolean): Done or not?
function TodoItem(text) {
    this.text = text;
    this.done = false;
}