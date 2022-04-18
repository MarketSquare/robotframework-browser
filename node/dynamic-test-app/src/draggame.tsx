import Draggable, { DraggableData, DraggableEvent } from 'react-draggable';
import React, { useState } from 'react';

// Remove after fix:
// https://github.com/react-grid-layout/react-draggable/pull/648#issuecomment-1100110050
declare module 'react-draggable' {
    export interface DraggableProps {
        children: React.ReactNode;
    }
}

export function DragGame() {
    const goal = {
        top: 500,
        left: 100,
        width: 130,
        height: 130,
    };
    const onCircleDrag = (e: DraggableEvent, position: DraggableData) => {
        const { x, y } = position;
        if (y >= 430 && y <= 465 && x >= 95 && x <= 130) {
            setCircleInTheGoal(true);
        }
        setCirclePosition({ x, y });
    };
    const [circlePosition, setCirclePosition] = useState({ x: 70, y: 70 });
    const [circleInTheGoal, setCircleInTheGoal] = useState(false);
    return (
        <div>
            <h2>{circleInTheGoal ? 'GOAL!!' : 'Put the circle in the goal'}</h2>
            <div className="game-area">
                <Draggable position={circlePosition} onDrag={onCircleDrag}>
                    <div
                        className="circle"
                        style={{
                            width: 100,
                            height: 100,
                            borderRadius: 50,
                            background: 'red',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            position: 'absolute',
                        }}
                    >
                        <span>Circle</span>
                    </div>
                </Draggable>
                <Draggable>
                    <div
                        className="obstacle"
                        style={{
                            width: 200,
                            height: 200,
                            background: 'blue',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            position: 'absolute',
                        }}
                    >
                        <span>Obstacle</span>
                    </div>
                </Draggable>
                <div
                    className="goal"
                    style={{
                        ...goal,
                        border: '3px solid black',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        position: 'absolute',
                        zIndex: -1,
                    }}
                >
                    <span>Goal</span>
                </div>
            </div>
        </div>
    );
}
