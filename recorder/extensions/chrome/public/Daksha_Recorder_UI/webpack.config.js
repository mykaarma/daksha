const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/ContentScript.js',
  output: {
    path: path.resolve(__dirname, 'public'),
    filename: 'ContentScript.js',
  },
};