import { HashRouter, Route, Switch } from 'react-router-dom';
import Login from './login';
import React from 'react';

function DragGame() {
    return <h2>FooBar!</h2>;
}

export default function App() {
    return (
        <HashRouter>
            <Switch>
                <Route path="/draggame">
                    <DragGame />
                </Route>
                <Route path="/">
                    <Login />
                </Route>
            </Switch>
        </HashRouter>
    );
}
