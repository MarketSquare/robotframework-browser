// Created by Copilot
// This code is a simple drag-and-drop game using React and react-dnd.
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import React, { useCallback, useEffect, useState } from 'react';

const ItemTypes = {
    CIRCLE: 'circle',
    BOX: 'box',
};

const DraggableItem = ({ id, type, x, y, onDrop, onLog }) => {
    const [{ isDragging }, drag] = useDrag(() => ({
        type,
        item: { id, type },
        collect: (monitor) => ({
            isDragging: monitor.isDragging(),
        }),
        end: (_, monitor) => {
            if (!monitor.didDrop()) {
                onLog(`Drag ended without drop for ${type} (${id}).`);
            }
        },
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
            onMouseDown={() => onLog(`Drag start for ${type} (${id}).`)}
        />
    );
};

const DropZone = ({ onDrop, onGoal, onLog }) => {
    const [, drop] = useDrop(() => ({
        accept: [ItemTypes.CIRCLE, ItemTypes.BOX],
        drop: (item, monitor) => {
            const offset = monitor.getClientOffset();
            if (!offset) {
                return undefined;
            }
            const isInGoal =
                offset.x >= 50 &&
                offset.x <= 150 &&
                offset.y >= window.innerHeight / 2 - 50 &&
                offset.y <= window.innerHeight / 2 + 50;

            onLog(`DropZone received ${item.type} (${item.id}) at (${Math.round(offset.x)}, ${Math.round(offset.y)}).`);
            if (isInGoal && item.type === ItemTypes.CIRCLE) {
                onLog('Circle entered goal.');
                onGoal();
                return { target: 'goal-post', offset };
            }
            onDrop(item.id, offset.x, offset.y);
            return { target: 'drop-zone', offset };
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

const InvisibleDropZone = ({ onDrop, onLog }) => {
    const [{ isOver }, drop] = useDrop(() => ({
        accept: [ItemTypes.CIRCLE, ItemTypes.BOX],
        drop: (item, monitor) => {
            const offset = monitor.getClientOffset();
            if (!offset) {
                return undefined;
            }
            onLog(
                `Invisible zone drop: ${item.type} (${item.id}) at (${Math.round(offset.x)}, ${Math.round(offset.y)}).`,
            );
            onDrop(item.id, offset.x, offset.y);
            return { target: 'invisible-element', offset };
        },
        collect: (monitor) => ({
            isOver: monitor.isOver({ shallow: true }),
        }),
    }));

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
                backgroundColor: isOver ? 'rgba(255, 165, 0, 0.15)' : 'transparent',
                border: isOver ? '2px solid orange' : '1px dashed gray',
            }}
        />
    );
};

const DragGame: React.FC = () => {
    const [items, setItems] = useState([
        { id: 1, type: ItemTypes.CIRCLE, x: window.innerWidth / 2 - 25, y: window.innerHeight / 2 - 25 }, // Red circle in the middle
        { id: 2, type: ItemTypes.BOX, x: window.innerWidth / 2 - 80, y: window.innerHeight / 2 - 80 }, // Blue box in the middle
    ]);
    const [goalMessage, setGoalMessage] = useState('Put the circle in the goal');
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        document.title = 'Drag game';
    }, []);

    const handleDrop = (id, x, y) => {
        setItems((prevItems) => prevItems.map((item) => (item.id === id ? { ...item, x, y } : item)));
    };

    const addLog = useCallback((entry: string) => {
        const timestamp = new Date().toISOString().split('T')[1]?.slice(0, 8);
        console.log(`[DragGame] ${entry}`);
        setLogs((prev) => [...prev.slice(-19), `${timestamp} ${entry}`]);
    }, []);

    const handleGoal = () => {
        setGoalMessage('GOAL!!!');
    };

    // Find the blue box's position
    const blueBox = items.find((item) => item.type === ItemTypes.BOX);

    return (
        <DndProvider backend={HTML5Backend}>
            <DropZone onDrop={handleDrop} onGoal={handleGoal} onLog={addLog} />
            {items.map((item) => (
                <DraggableItem
                    key={item.id}
                    id={item.id}
                    type={item.type}
                    x={item.x}
                    y={item.y}
                    onDrop={handleDrop} // Pass the drop handler
                    onLog={addLog}
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
            <InvisibleDropZone onDrop={handleDrop} onLog={addLog} />
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
            <div
                id="debug-log"
                style={{
                    position: 'absolute',
                    bottom: 20,
                    left: 20,
                    width: '320px',
                    maxHeight: '200px',
                    overflowY: 'auto',
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    color: 'white',
                    padding: '10px',
                    borderRadius: '6px',
                    fontSize: '12px',
                    lineHeight: '1.4',
                }}
            >
                <div style={{ fontWeight: 'bold', marginBottom: '6px' }}>Debug log</div>
                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {logs.map((log, index) => (
                        <li key={`${log}-${index}`} style={{ marginBottom: '4px' }}>
                            {log}
                        </li>
                    ))}
                </ul>
            </div>
        </DndProvider>
    );
};

export default DragGame;
