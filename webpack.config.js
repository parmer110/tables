const path = require('path');

module.exports = {
  mode: 'development',
  entry: {
    common_index: './common/static/js/common_index.js',
    modal: './common/static/js/components.js',
    register: './common/static/js/common_register.js',
  },
  output: {
    path: path.resolve(__dirname, './common/static/dist'),
    filename: '[name]_bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
      // new CSS rule
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
};
