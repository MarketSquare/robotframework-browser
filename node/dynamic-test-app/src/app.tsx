import { HashRouter, Route, Routes } from 'react-router-dom';
import DragGame from './draggame';
import Login from './login';
import React from 'react';

const App: React.FC = () => {
    return (
        <HashRouter>
            {/* Add other components or content here */}
            <Routes>
                <Route path="/draggame" element={<DragGame />} />
                <Route path="/" element={<Login />} />
            </Routes>
        </HashRouter>
    );
};

export default App;
