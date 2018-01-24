const path = require('path');

module.exports = {
    entry: "./src/todo.js", // string | object | array
    // Here the application starts executing
    // and webpack starts bundling

    output: {
        // options related to how webpack emits results

        path: path.resolve(__dirname, "dist"), // string
        // the target directory for all output files
        // must be an absolute path (use the Node.js path module)

        filename: "bundle.js", // string
        // the filename template for entry chunks

        publicPath: "/dist/", // string
        // the url to the output directory resolved relative to the HTML page
    },

    module: {
        rules: [
          {
            test: /\.css$/,
            use: [ 'style-loader', 'css-loader' ]
          }
        ]
    }
}