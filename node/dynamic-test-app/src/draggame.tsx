// Created by Copilot
// This code is a simple drag-and-drop game using React and react-dnd.
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import React, { useEffect, useState } from 'react';

const ItemTypes = {
    CIRCLE: 'circle',
    BOX: 'box',
};

const DraggableItem = ({ id, type, x, y, onDrop }) => {
    const [{ isDragging }, drag] = useDrag(() => ({
        type,
        item: { id, type },
        collect: (monitor) => ({
            isDragging: monitor.isDragging(),
        }),
    }));

    const [, drop] = useDrop(() => ({
        accept: [ItemTypes.CIRCLE, ItemTypes.BOX],
        drop: (item, monitor) => {
            const offset = monitor.getClientOffset();
            if (offset) {
                onDrop(item.id, offset.x, offset.y);
            }
        },
    }));

    return (
        <div
            ref={(node) => drag(drop(node))} // Combine drag and drop refs
            id={type === ItemTypes.CIRCLE ? 'red-circle' : 'blue-box'}
            style={{
                position: 'absolute',
                left: x,
                top: y,
                width: type === ItemTypes.CIRCLE ? 50 : 160,
                height: type === ItemTypes.CIRCLE ? 50 : 160,
                backgroundColor: type === ItemTypes.CIRCLE ? 'red' : 'blue',
                borderRadius: type === ItemTypes.CIRCLE ? '50%' : '0',
                opacity: isDragging ? 0.5 : 1,
                cursor: 'move',
            }}
        />
    );
};

const DropZone = ({ onDrop, onGoal }) => {
    const [, drop] = useDrop(() => ({
        accept: [ItemTypes.CIRCLE, ItemTypes.BOX],
        drop: (item, monitor) => {
            const offset = monitor.getClientOffset();
            if (offset) {
                const isInGoal = offset.x >= 50 && offset.x <= 150 && offset.y >= window.innerHeight / 2 - 50 && offset.y <= window.innerHeight / 2 + 50;

                if (isInGoal && item.type === ItemTypes.CIRCLE) {
                    onGoal();
                } else {
                    onDrop(item.id, offset.x, offset.y);
                }
            }
        },
    }));

    return (
        <div
            ref={drop}
            style={{
                position: 'relative',
                width: '100vw',
                height: '100vh',
                border: '1px solid black',
            }}
        >
            <div
                id="goal-post"
                style={{
                    position: 'absolute',
                    left: 50,
                    top: window.innerHeight / 2 - 50,
                    width: 100,
                    height: 100,
                    backgroundColor: 'yellow',
                    border: '2px dashed black',
                }}
            >
                Goal
            </div>
        </div>
    );
};

const InvisibleDropZone = ({ onDrop }) => {
    const [, drop] = useDrop(() => ({
        accept: [ItemTypes.CIRCLE, ItemTypes.BOX],
        drop: (item, monitor) => {
            const offset = monitor.getClientOffset();
            if (offset) {
                onDrop(item.id, offset.x, offset.y);
            }
        },
    }));

    const [isDragging, setIsDragging] = useState(false);

    return (
        <div
            ref={drop}
            id="invisible-element"
            style={{
                position: 'absolute',
                top: 100,
                left: '50%',
                transform: 'translateX(-50%)',
                width: '200px',
                height: '50px',
                backgroundColor: 'transparent',
                border: '1px dashed gray',
                pointerEvents: isDragging ? 'none' : 'auto', // Disable pointer events during drag
            }}
            onDragEnter={() => setIsDragging(true)} // Detect drag start
            onDragLeave={() => setIsDragging(false)} // Detect drag end
        />
    );
};

const DragGame = () => {
    const [items, setItems] = useState([
        { id: 1, type: ItemTypes.CIRCLE, x: window.innerWidth / 2 - 25, y: window.innerHeight / 2 - 25 }, // Red circle in the middle
        { id: 2, type: ItemTypes.BOX, x: window.innerWidth / 2 - 80, y: window.innerHeight / 2 - 80 }, // Blue box in the middle
    ]);
    const [goalMessage, setGoalMessage] = useState('Put the circle in the goal');

    useEffect(() => {
        document.title = 'Drag game';
    }, []);

    const handleDrop = (id, x, y) => {
        setItems((prevItems) => prevItems.map((item) => (item.id === id ? { ...item, x, y } : item)));
    };

    const handleGoal = () => {
        setGoalMessage('GOAL!!!');
    };

    // Find the blue box's position
    const blueBox = items.find((item) => item.type === ItemTypes.BOX);

    return (
        <DndProvider backend={HTML5Backend}>
            <DropZone onDrop={handleDrop} onGoal={handleGoal} />
            {items.map((item) => (
                <DraggableItem
                    key={item.id}
                    id={item.id}
                    type={item.type}
                    x={item.x}
                    y={item.y}
                    onDrop={handleDrop} // Pass the drop handler
                />
            ))}
            <h2
                style={{
                    position: 'absolute',
                    top: 20,
                    left: '50%',
                    transform: 'translateX(-50%)',
                    fontSize: '24px',
                    fontWeight: 'bold',
                    color: goalMessage === 'GOAL!!!' ? 'green' : 'black',
                }}
            >
                {goalMessage}
            </h2>
            <InvisibleDropZone onDrop={handleDrop} />
            <div
                id="blue-box-coordinates"
                style={{
                    position: 'absolute',
                    top: 20,
                    right: 20,
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: 'blue',
                    backgroundColor: 'white',
                    padding: '10px',
                    border: '1px solid black',
                    borderRadius: '5px',
                }}
            >
                <div
                    id="blue-box-x-row"
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px', // Add spacing between text and value
                    }}
                >
                    <div id="blue-box-x-text">Blue Box X:</div>
                    <div id="blue-box-x-value">{blueBox ? blueBox.x : 'Not Found'}</div>
                </div>
                <div
                    id="blue-box-y-row"
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px', // Add spacing between text and value
                    }}
                >
                    <div id="blue-box-y-text">Blue Box Y:</div>
                    <div id="blue-box-y-value">{blueBox ? blueBox.y : 'Not Found'}</div>
                </div>
            </div>
        </DndProvider>
    );
};

export default DragGame;
