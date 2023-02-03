import { DragGame } from './draggame';
import { HashRouter, Route, Routes } from 'react-router-dom';
import Login from './login';
import React from 'react';

export default function App() {
    return (
        <HashRouter>
            <Routes>
                <Route path="/draggame" element={<DragGame />} />
                <Route path="/" element={<Login />} />
            </Routes>
        </HashRouter>
    );
}
