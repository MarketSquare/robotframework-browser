# robotframework-browser

This example shows how to translate more modern ECMAScript 2015+ javascript modules to CommonJS.
The example uses [Babel](https://babeljs.io/) to translate es2015 `index.js` file in `src` folder to CommonJS file in lib `folder`.

To run the exmaple translation and to show the relevant documentation do:
```
npm install
npm run build
python -m robot.libdoc Browser::jsextension=lib/index.js show funkkari
```
