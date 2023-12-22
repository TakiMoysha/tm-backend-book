const path = require("path");

module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "js/native-bundle.js",
    path: path.resolve(__dirname, "../static-dev"),
  },
};
