import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import Webcam from "react-webcam";

// Define the possible Rubik's colors + an optional grey
const rubikColors = ["white", "yellow", "green", "blue", "red", "orange", "grey"];

// We’ll define the initial 3x3 faces so that only centers are colored
// and everything else is grey. The index 4 in each 3x3 array is the center.
const initialCubeState = {
  // index 4 is center
  up:    ["grey","grey","grey","grey","yellow","grey","grey","grey","grey"],
  down:  ["grey","grey","grey","grey","white","grey","grey","grey","grey"],
  front: ["grey","grey","grey","grey","green","grey","grey","grey","grey"],
  left:  ["grey","grey","grey","grey","red","grey","grey","grey","grey"],
  right: ["grey","grey","grey","grey","orange","grey","grey","grey","grey"],
  back:  ["grey","grey","grey","grey","blue","grey","grey","grey","grey"],
};

// A small helper to style a single square
function getSquareStyle(color) {
  return {
    width: "40px",
    height: "40px",
    backgroundColor: color,
    border: "1px solid #222",
    boxSizing: "border-box",
    cursor: "pointer",
    position: "relative",
  };
}

// A Face component to render one 3x3 face
// We pass down a handleClickSquare callback to open the color picker
function Face({ faceName, squares, handleClickSquare }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 40px)",
        margin: "5px",
      }}
    >
      {squares.map((color, idx) => (
        <div
          key={idx}
          style={getSquareStyle(color)}
          onClick={(e) => handleClickSquare(faceName, idx, e)}
        />
      ))}
    </div>
  );
}

// A simple popup color picker. This can be replaced with a fancier library if desired.
function ColorPickerPopup({ x, y, onPickColor, onClose }) {
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: x,
        backgroundColor: "white",
        border: "1px solid #333",
        borderRadius: "4px",
        padding: "8px",
        zIndex: 9999,
      }}
    >
      <div style={{ display: "flex", flexWrap: "wrap", gap: "5px" }}>
        {rubikColors.map((color) => (
          <div
            key={color}
            onClick={() => onPickColor(color)}
            style={{
              width: "30px",
              height: "30px",
              backgroundColor: color,
              border: "1px solid #222",
              cursor: "pointer",
            }}
          />
        ))}
      </div>
      <button
        style={{ marginTop: "8px", width: "100%" }}
        onClick={onClose}
      >
        Cancel
      </button>
    </div>
  );
}

// A simple modal for instructions
function InstructionsModal({ open, onClose }) {
  if (!open) return null;

  return (
    <div 
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 10000
      }}
    >
      <div 
        style={{
          backgroundColor: "#fff",
          borderRadius: "8px",
          padding: "20px",
          maxWidth: "500px",
          width: "90%",
          boxShadow: "0 2px 10px rgba(0,0,0,0.3)",
        }}
      >
        <h2 style={{ marginTop: 0 }}>Instructions</h2>
        {/* Replace this placeholder text with your real instructions */}
        <p>Due to the fact that the direction of photo matters in this context, the solver will only work with the following set of instructions for direction of photo for each face.</p>
        <p>1. Place the cube with the yellow face up, and the white face down.</p>
        <p>Try to position your camera such that most of the video feed is covered by the cube. Additionally, try to be in a well lit room without too much glare.</p>
        <p>2. Take photos of the green, red, orange, and blue faces all in such a way that the yellow face is up, and white face down.</p>
        <p>3. Take photos of the yellow face with the blue face up, and green face down.</p>
        <p>3. Take photos of the white face with the green face up, and blue face down.</p>
        <p>Note: As the hues and lighting of each Rubik's cube/photo may differ, the machine learning model may have slight inaccuracies while detecting faces. Hence, it is always a good idea to check the virtual cube with your actual cube for any discrepancies. You can always change individual colors of each face by clicking on their respective squares.</p>
        <p>4. When each face is filled up, the "solve cube" button will appear. Clicking that button will make it so that if you check the solver page linked on the bottom, it will redirect you to the page detailing the specific scramble you gave and its solution.</p>
        <button 
          onClick={onClose} 
          style={{ marginTop: "10px", padding: "8px 16px", cursor: "pointer" }}
        >
          Close
        </button>
      </div>
    </div>
  );
}

function Tmp() {
  const [cubeState, setCubeState] = useState(initialCubeState);
  const webcamRef = useRef(null);
  const [response, setResponse] = useState(null);

  // For the popup color picker
  const [pickerOpen, setPickerOpen] = useState(false);
  const [pickerPosition, setPickerPosition] = useState({ x: 0, y: 0 });
  const [selectedFace, setSelectedFace] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);

  // For instructions modal
  const [showInstructions, setShowInstructions] = useState(false);

  useEffect(() => {
    if (response) {
      localStorage.setItem("response", JSON.stringify(response));
    }
  }, [response]);

  // This function updates the cubeState with recognized colors from the backend
  const updateFaceColors = (faceName, recognizedColors) => {
    setCubeState((prev) => ({
      ...prev,
      [faceName]: recognizedColors,
    }));
  };

  // “Take photo” and send to backend
  const capturePhoto = async () => {
    if (!webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    console.log("Captured photo, sending to backend...");

    // Example request body
    const body = { image: imageSrc };

    // Send the image to your backend for ML inference
    try {
      const response = await fetch("/recognize-face", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await response.json();

      // Suppose the backend returns something like:
      // {
      //   faceName: 'front',
      //   colors: ['white','white','blue','orange','green','red','yellow','blue','green']
      // }
      if (data.faceName && data.colors) {
        updateFaceColors(data.faceName, data.colors);
      }
    } catch (error) {
      console.error("Error recognizing face", error);
    }
  };

  // “Solve” the fully-updated cube
  const solveCube = async () => {
    console.log("Sending full cube state to backend for solve...");

    // Save a copy of the layout in local storage
    localStorage.setItem("lastCubeLayout", JSON.stringify(cubeState));

    try {
      const response = await fetch("/solve-cube", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cubeState),
      });
      const data = await response.json();
      console.log("Solution response:", data);
      setResponse(data);
      // handle solution result, e.g. show step-by-step instructions
    } catch (error) {
      console.error("Error solving cube", error);
    }
  };

  // Handle click on a square: open the popup color picker
  const handleClickSquare = (faceName, index, event) => {
    // Disallow changing center squares
    if (index === 4) return;

    // Position the popup near the clicked square
    const rect = event.target.getBoundingClientRect();
    const x = rect.left + window.scrollX + rect.width + 10; // slight offset
    const y = rect.top + window.scrollY;

    setSelectedFace(faceName);
    setSelectedIndex(index);
    setPickerPosition({ x, y });
    setPickerOpen(true);
  };

  // Once user picks a color in the popup
  const handlePickColor = (color) => {
    if (!selectedFace || selectedIndex === null) return;

    // Replace the color in that face's array
    setCubeState((prev) => {
      const newFace = [...prev[selectedFace]];
      newFace[selectedIndex] = color;
      return {
        ...prev,
        [selectedFace]: newFace,
      };
    });

    // Close the popup
    setPickerOpen(false);
  };

  const handleClosePicker = () => {
    setPickerOpen(false);
  };

  // Check if every square is non-grey
  const isCubeFilled = () => {
    const allFaces = Object.values(cubeState); // array of 6 arrays
    for (let face of allFaces) {
      if (face.includes("grey")) {
        return false;
      }
    }
    return true;
  };

  // Layout Styles
  const containerStyle = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    margin: "20px",
  };

  const leftColumnStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "45%",
  };

  const rightColumnStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "45%",
    backgroundColor: "#f5f5f5",
    borderRadius: "8px",
    padding: "10px",
  };

  const buttonContainerStyle = {
    marginTop: "15px",
    display: "flex",
    gap: "10px",
  };

  return (
    <div style={{ fontFamily: "sans-serif" }}>
      {/* Instructions Modal */}
      <InstructionsModal
        open={showInstructions}
        onClose={() => setShowInstructions(false)}
      />

      <h2 style={{ textAlign: "center", marginTop: "20px" }}>
        Rubik’s Cube Camera Page
      </h2>

      <div style={containerStyle}>
        {/* Left Column: Webcam and Buttons */}
        <div style={leftColumnStyle}>

          <div style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "10px" }}>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={400}
              height={300}
              style={{ borderRadius: "4px" }}
            />
          </div>

          <div style={buttonContainerStyle}>
            <button onClick={capturePhoto}>Capture Photo</button>

            {/* Only show "Solve Cube" if the entire cubeState is filled (no "grey") */}
            {isCubeFilled() && (
              <button onClick={solveCube}>Solve Cube</button>
            )}

            <button onClick={() => setShowInstructions(true)}>
              Show Instructions
            </button>
          </div>

          <Link to="/solver" style={{ marginTop: "15px" }}>
            Go to Solver Page
          </Link>
        </div>

        {/* Right Column: Cube Net Layout */}
        <div style={rightColumnStyle}>
          <h3 style={{ marginTop: "0" }}>Your Cube State</h3>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            {/* Up face */}
            <Face
              faceName="up"
              squares={cubeState.up}
              handleClickSquare={handleClickSquare}
            />

            <div style={{ display: "flex", justifyContent: "center" }}>
              <Face
                faceName="left"
                squares={cubeState.left}
                handleClickSquare={handleClickSquare}
              />
              <Face
                faceName="front"
                squares={cubeState.front}
                handleClickSquare={handleClickSquare}
              />
              <Face
                faceName="right"
                squares={cubeState.right}
                handleClickSquare={handleClickSquare}
              />
              <Face
                faceName="back"
                squares={cubeState.back}
                handleClickSquare={handleClickSquare}
              />
            </div>

            {/* Down face */}
            <Face
              faceName="down"
              squares={cubeState.down}
              handleClickSquare={handleClickSquare}
            />
          </div>
        </div>
      </div>

      {/* Render the color picker if open */}
      {pickerOpen && (
        <ColorPickerPopup
          x={pickerPosition.x}
          y={pickerPosition.y}
          onPickColor={handlePickColor}
          onClose={handleClosePicker}
        />
      )}
    </div>
  );
}

export default Tmp;
