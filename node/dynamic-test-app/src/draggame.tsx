// Created by Copilot
// This code is a simple drag-and-drop game using React and react-dnd.
import React, { useState, useEffect } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

const ItemTypes = {
  CIRCLE: "circle",
  BOX: "box",
};

const DraggableItem = ({ id, type, x, y }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type,
    item: { id, type },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div
      id={type === ItemTypes.CIRCLE ? "red-circle" : "blue-box"} // Add id for red circle and blue box
      ref={drag}
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: type === ItemTypes.CIRCLE ? 50 : 160, // Doubled width for blue box
        height: type === ItemTypes.CIRCLE ? 50 : 160, // Doubled height for blue box
        backgroundColor: type === ItemTypes.CIRCLE ? "red" : "blue",
        borderRadius: type === ItemTypes.CIRCLE ? "50%" : "0",
        opacity: isDragging ? 0.5 : 1,
        cursor: "move",
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
        const isInGoal =
          offset.x >= 300 &&
          offset.x <= 400 &&
          offset.y >= 300 &&
          offset.y <= 400;

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
        position: "relative",
        width: "100vw",
        height: "100vh",
        border: "1px solid black",
      }}
    >
      <div
        id="goal" // Add id for the goal
        style={{
          position: "absolute",
          left: 300,
          top: 300,
          width: 100,
          height: 100,
          backgroundColor: "yellow",
          border: "2px dashed black",
        }}
      >
        Goal
      </div>
    </div>
  );
};

const Game = () => {
  const [items, setItems] = useState([
    { id: 1, type: ItemTypes.CIRCLE, x: 10, y: 10 }, // Red circle
    { id: 2, type: ItemTypes.BOX, x: 10, y: -70 }, // Blue box starts entirely above the red circle
  ]);
  const [goalMessage, setGoalMessage] = useState("Put the circle in the goal");

  useEffect(() => {
    document.title = "Drag game"; // Set the page title
  }, []);

  const handleDrop = (id, x, y) => {
    setItems((prevItems) =>
      prevItems.map((item) =>
        item.id === id ? { ...item, x, y } : item
      )
    );
  };

  const handleGoal = () => {
    setGoalMessage("GOAL!!!");
  };

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
        />
      ))}
      <h2
        style={{
          position: "absolute",
          top: 20,
          left: "50%",
          transform: "translateX(-50%)",
          fontSize: "24px",
          fontWeight: "bold",
          color: goalMessage === "GOAL!!!" ? "green" : "black",
        }}
      >
        {goalMessage}
      </h2>
      <div
        id="invisible-element"
        style={{
          position: "absolute",
          top: 60, // Adjusted to be below the h2 element
          left: "50%",
          transform: "translateX(-50%)",
          width: "100px",
          height: "20px",
          visibility: "hidden", // Makes the element invisible
        }}
      >
        Invisible Element
      </div>
    </DndProvider>
  );
};

export default Game;