/**
 *
 * Musterlösung Blatt 5
 *
 * Erweitern Sie den Icon-Editor um folgende Funktionen:

- Malen: Statt nur mit einzelnen Clicks auf Einzelzellen soll auch gemalt werden
  können, indem Sie mit gedrückter Maustaste über die Tabelle fahren und dabei
  alle berührten Zellen färben.
- Füllen: Es soll ein "Fill mode" aktiviert werden können, der nicht nur eine einzelne Zelle färbt,
  sondern die angeklickte Zelle und (rekursiv) alle benachbarten Zellen mit der gleichen Farbe. Bei aktiviertem
  Füllmodus soll ein anderer, das Füllen symbolisierende Mouse-Cursor verwendet werden.
  (Tipp: `document.body.style.cursor = "url('/url/to/required/image.jpg')";`)
- Pinselbreite: Führen Sie die Eigenschaft "Pinselbreite" ein, die regelt, wie groß die
  gesetzten Punkte (derzeit immer 1x1 Zellen/Pixel) sind. Mit einem Schieberegler (Tipp: <input type="range">)
  soll es möglich sein, für die Pinselbreite einen Wert zwischen 1 und 10 einzustellen, der dann dergestalt
  berücksichtigt wird, dass ein Klick anschließend n x n Zellen/Pixel große Punkte erzeugt, wobei der Klickpunkt
  links oben im entstehenden Quadrat ist.
- Icons laden: Es soll rein clientseitig möglich sein, eines der unter "vorhandene Icons" angezeigten Icons
  per Klick in den Editor zu übernehmen, um es zu bearbeiten und unter gleichem oder neuem Namen zu speichern.
  (Sie müssen dazu ein Image-Objekt erstellen, das mit der Data-URL als Quelle versehen wird und nach dem Laden
  dieser Quelle auf den Canvas-Kontext angezeigt wird. Anschließend können Sie die Pixel per getImageData auslesen)

 */

function create_table() {
    var tablediv=document.getElementById('icon-table');
    var table = document.createElement("table");
    table.className = "icon-table";
    tablediv.appendChild(table);
    for (var i = 0; i < 16; i++) {
        var tr = document.createElement("tr");
        table.appendChild(tr);
        for (var j = 0; j < 16; j++) {
            var td = document.createElement("td");
            td.className = "icon-pixel";
            td.id="pixel-"+ i + "-" + j;
            td.style.backgroundColor = "rgb(255,255,255)"; // no dash - css attribute name becomes camelCase
            td.addEventListener("mouseover", setpixel_if_drawing);
            td.addEventListener("click", setpixel);
            tr.appendChild(td);
        }
    }
}

/* construct the color picker table */
function create_color_picker() {
    var tablediv = document.getElementById('color-picker');
    var table = document.createElement("table"); // create table
    table.className = "color-picker-table"; // assign css class
    tablediv.appendChild(table); // hang the table into the page dom tree
    var tr;
    var count = 0;
    var step = 63; // step width for picker generation. smaller width means more colors
    for (var r=0; r < 256; r += step) {
        for (var g=0; g < 256; g += step) {
            for (var b = 0; b < 256; b += step) {
                if (count++ % 24 === 0) {  // new row
                    tr = document.createElement("tr");
                    table.appendChild(tr);
                }
                var td = document.createElement("td"); // new cell
                td.className = "picker-pixel";
                td.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
                td.addEventListener("click", choosecolor); // register click callback
                tr.appendChild(td);
            }
        }
    }
    // register callbacks for specials brushes
    // document.getElementById("bw-switcher").addEventListener("click", choose_bw_switcher);
    // document.getElementById("random").addEventListener("click", choose_random_brush);
    document.getElementById("mode-paint").addEventListener("click", choose_mode_paint);
    document.getElementById("mode-fill").addEventListener("click", choose_mode_fill);
}

/* click callback for selection one color */
function choosecolor(event) {
    var currentColor=document.getElementById("current-color");
    currentColor.innerHTML="&nbsp;&nbsp;&nbsp;";
    currentColor.style.backgroundColor = this.style.backgroundColor;
    currentColor.removeAttribute("data-mode");
}

/* click callback for fill brush tool */
function choose_mode_fill(event) {
    mode = 'fill';
    document.getElementById('icon-table').classList.remove('mode-paint');
    document.getElementById('icon-table').classList.add('mode-fill');
    document.getElementById('mode-paint').classList.remove('active');
    document.getElementById('mode-fill').classList.add('active');
}

/* click callback for paint brush tool */
function choose_mode_paint(event) {
    mode = 'paint';
    document.getElementById('icon-table').classList.remove('mode-fill');
    document.getElementById('icon-table').classList.add('mode-paint');
    document.getElementById('mode-fill').classList.remove('active');
    document.getElementById('mode-paint').classList.add('active');
}


/* Global mode variables */
var mode = 'paint';  // other values: 'fill'
var pixel_drawing = false;

function setpixel_draw(event) {
    pixel_drawing = true;
    setpixel_if_drawing(event);  // also draw first cell, as mouseover will only occur for next cell
}

function setpixel_nodraw(event) {
    pixel_drawing = false;
}

function setpixel_if_drawing(event) {
    if (!pixel_drawing) return;
    setpixel(event);
}

/* set pixels using current brush (color, mode, width) after click */
function setpixel(event) {

    if (mode=='fill') {
        return fillpixel(event);
    }

    var cc = document.getElementById("current-color"); // current color element contains color
    if (cc.hasAttribute('data-mode')) mode=cc.getAttribute('data-mode');
    var m = event.target.id.match(/pixel-([0-9]+)-([0-9]+)/i); // matchgroups m[1] and m[2] contain coordinates
    if (m) {
        var x = parseInt(m[1]); // must be explicitly converted, otherwise x+w in for loop would be concatenated string
        var y = parseInt(m[2]);
        var w = get_brushwidth();
        for (var i=x; i<16 && i<x+w; i++) { // two loops to walk around the matrix
            for (var j=y; j<16 && j<y+w; j++) {
               var pixel = document.getElementById("pixel-" + i + "-" + j);
               // set pixel to currently selected color
               pixel.style.backgroundColor = cc.style.backgroundColor;
            }
        }
    }
    preview();  // update preview
}


/* flood fill from clicked cell

   non-recursive implementation with to queues:
   1. tovisit: all pixels that we have to check
   2. visited: all pixels that we already checked

   the algorithm starts at the clicked pixel and add it to tovisit

   while tovisit is not empty:

       remove first element from tovisit and add it to visited

       if it has the same color than the clicked pixel
             and is not in visited or tovisit:
          fill it in the desired color
          add all neighbors to tovisit

 */
function fillpixel(event) {

    var m = event.target.id.match(/pixel-([0-9]+)-([0-9]+)/i); // matchgroups m[1] and m[2] contain coordinates
    if (m) {  // if we clicked a pixel

        // val is a number 0 <= val <= 255, return an object with properties x and y for coordinates
        function to_coords(val) {
            return {'x': val % 16,
                    'y': Math.floor(val/16) };
        }

        // take coordinates and return a number 0 <= val <= 255 to represent coordinates as an integer
        function from_coords(x,y) {
            return x + y*16;
        }

        // return color at given pixel
        function color_at(x,y) {
            console.log("x="+x+", y="+y+", id=pixel-"+x+"-"+y);
            return document.getElementById("pixel-"+x+"-"+y).style.backgroundColor;
        }

        var visited=[];  // list of pixels we already finished looking at
        var tovisit=[];  // list of pixel that we have to look at yet
        var current_color = document.getElementById("current-color").style.backgroundColor;// current color element contains color
        var x = parseInt(m[1]); // must be explicitly converted, otherwise x+w in for loop would be concatenated string
        var y = parseInt(m[2]);
        var color = color_at(x,y);  // the color the pixel to be filled had before - we look for connected cells with this color

        tovisit.push(from_coords(x,y));

        while (tovisit.length) {  // while there are still pixels to look at
            var cur = tovisit.shift();  // pick the first pixel
            visited.push(cur);  // add it to the visited list (never visit again)
            var curx = to_coords(cur).x;
            var cury = to_coords(cur).y;
            if (color_at(curx, cury) == color) {
                // if this pixel has the same color as the first pixel clicked:
                // 1. we fill ist
                // 2. we add its neighbors to the tovisit list
                document.getElementById("pixel-" + curx + "-" + cury).style.backgroundColor = current_color;  // fill it
                // each cell has 4 neighbors: left, right, up, down
                var new_coords = [];
                if (curx>0) new_coords.push(from_coords(curx-1,cury));
                if (curx<15) new_coords.push(from_coords(curx+1, cury));
                if (cury<15) new_coords.push(from_coords(curx, cury+1));
                if (cury>0) new_coords.push(from_coords(curx, cury-1));

                // we check for each neighbor if it is in bounds and not visited yet -> add to tovisit list.
                for (var i = 0; i < new_coords.length; i++) {
                    var c = to_coords(new_coords[i]);
                    if (visited.indexOf(new_coords[i]) == -1 && tovisit.indexOf(new_coords[i]) == -1) {
                        tovisit.push(new_coords[i]);
                    }
                }
            }
        }
    }
    return preview(); // update preview
}

/* create a preview image on a canvas */
function preview() {
    var canvas = document.getElementById('preview-canvas');
    var ctx = canvas.getContext("2d");
    for (var i=0; i<16; i++) {
        for (var j=0; j<16; j++) {
            ctx.fillStyle = document.getElementById("pixel-"+i+"-"+j).style.backgroundColor;
            ctx.fillRect(j,i,1,1);
        }
    }
    document.getElementById("save-icon").value = canvas.toDataURL();
}

/* display value of range-input element as number */
function display_brushwidth(event) {
    document.querySelector("#brush-width-display").innerHTML = get_brushwidth();
}

/* return value of range-input element for setting the brush width */
function get_brushwidth() {
    return parseInt(document.querySelector("#brush-width").value);
}

/* load an icon from server generated icon list to preview canvas and pixel editor */
function load_icon(event) {

    // we need to do two steps:
    // 1. draw the image object to the canvas
    // 2. loop the canvas pixels and set pixel editor background colors

    var canvas = document.getElementById('preview-canvas');
    var ctx = canvas.getContext("2d");

    ctx.drawImage(event.target, 0, 0); // "event.target" is an Image object that can be drawn to the canvas
    for (var i=0; i<16; i++) { // loop through all the pixels
        for (var j=0; j<16; j++) {
            // getImageData returns a flat list with rgba (a=alpha) values
            // so rgba holds [r,g,b,a]
            var rgba = ctx.getImageData(j, i, 1, 1).data;
            // set backgroundColor property in editor table
            document.getElementById("pixel-"+i+"-"+j).style.backgroundColor = "rgb("+rgba[0]+","+rgba[1]+","+rgba[2]+")";
        }
    }
    document.getElementById("save-title").value = event.target.title;
}

/* add a click callback to every icon in server generated list of saved icons */
function register_iconlist_callback() {
    var icons = document.querySelectorAll("footer .icon-list-item img");
    for (var i=0; i<icons.length; i++) {
        icons[i].addEventListener("click", load_icon);
    }
}


window.onload = function () {
    validate_init(); // prepare form validation
    create_table(); // construct large pixel table
    create_color_picker(); // construct color picker and special brushes
    window.addEventListener("mousedown",setpixel_draw, true);
    window.addEventListener("mouseup", setpixel_nodraw, true);
    document.querySelector("#brush-width").addEventListener("input", display_brushwidth); // register callback for range input for brush width
    register_iconlist_callback(); // make icons from server clickable
    display_brushwidth(); // show the current brush width
    preview(); // construct and show a preview image
}

