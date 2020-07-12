import * as ReactDOM from "react-dom";
import * as React from "react";
import App from "./app"

window.__SET_RFBROWSER_STATE__ && window.__SET_RFBROWSER_STATE__({a:"HELLO FROM PAGE!", b:123});
ReactDOM.render(
    <App />,
    document.getElementById('root')
);
