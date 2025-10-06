import { HashRouter, Route, Routes } from 'react-router-dom';
import DragGame from './draggame';
import Login from './login';
import EventsPage from './events';
import React from 'react';

const App: React.FC = () => {
    return (
        <HashRouter>
            <Routes>
                <Route path="/draggame" element={<DragGame />} />
                <Route path="/events" element={<EventsPage />} />
                <Route path="/" element={<Login />} />
            </Routes>
        </HashRouter>
    );
};

export default App;
