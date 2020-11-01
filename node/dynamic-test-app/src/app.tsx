import { DragGame } from './draggame';
import { HashRouter, Route, Switch } from 'react-router-dom';
import Login from './login';
import React from 'react';

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
