"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
function Site() {
    var username = react_1.useRef("");
    var password = react_1.useRef("");
    var _a = react_1.useState(false), submit = _a[0], setSubmit = _a[1];
    var handleSubmit = function () {
        setSubmit(true);
    };
    function usernameChange(event) {
        username.current = event.target.value;
    }
    function passwordChange(event) {
        password.current = event.target.value;
    }
    function Body() {
        if (submit)
            return react_1.default.createElement(PostSubmit, null);
        else
            return react_1.default.createElement(PreSubmit, null);
    }
    function PreSubmit() {
        document.title = "Login Page";
        return react_1.default.createElement(react_1.default.Fragment, null,
            react_1.default.createElement("h1", null, "Login Page"),
            react_1.default.createElement("p", null, "Please input your user name and password and click the login button."),
            react_1.default.createElement("form", { name: "login_form", onSubmit: handleSubmit },
                react_1.default.createElement("table", null,
                    react_1.default.createElement("tbody", null,
                        react_1.default.createElement("tr", null,
                            react_1.default.createElement("td", null,
                                react_1.default.createElement("label", { htmlFor: "username_field" }, "User Name:")),
                            react_1.default.createElement("td", null,
                                react_1.default.createElement("input", { id: "username_field", size: 30, type: "text", onChange: usernameChange }))),
                        react_1.default.createElement("tr", null,
                            react_1.default.createElement("td", null,
                                react_1.default.createElement("label", { htmlFor: "password_field" }, "Password:")),
                            react_1.default.createElement("td", null,
                                react_1.default.createElement("input", { id: "password_field", size: 30, type: "password", onChange: passwordChange }))),
                        react_1.default.createElement("tr", null,
                            react_1.default.createElement("td", null),
                            react_1.default.createElement("td", null,
                                react_1.default.createElement("input", { id: "login_button", type: "submit", value: "LOGIN" })))))));
    }
    function PostSubmit() {
        if (username.current == "demo" && password.current == "mode") {
            document.title = "Welcome Page";
            return (react_1.default.createElement(react_1.default.Fragment, null,
                react_1.default.createElement("h1", null, "Welcome Page"),
                react_1.default.createElement("p", null,
                    "Login succeeded. Now you can ",
                    react_1.default.createElement("a", { href: "." }, "logout"),
                    ".")));
        }
        else {
            document.title = "Error Page";
            return (react_1.default.createElement(react_1.default.Fragment, null,
                react_1.default.createElement("h1", null, "Error Page"),
                react_1.default.createElement("p", null, "Login failed. Invalid user name and/or password.")));
        }
    }
    return react_1.default.createElement(Body, null);
}
exports.default = Site;
//# sourceMappingURL=app.js.map