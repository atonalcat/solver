import React, { useState } from 'react';
import './App.css';
import { Link } from "react-router-dom";

// 1) A color mapping from single-letter -> full color name
const colorMap = {
  "w": "white",
  "y": "yellow",
  "g": "green",
  "b": "blue",
  "r": "red",
  "o": "orange"
};

// 2) Convert the 2D array from the backend into an object of faces
//    { up: [...], left: [...], front: [...], right: [...], back: [...], down: [...] }
function convert2DToCubeState(twoD) {
  // Expecting twoD to be an array of length 6, each an array of length 9:
  //   [0] = up, [1] = left, [2] = front, [3] = right, [4] = back, [5] = down
  // We convert each single-letter to the color word

  return {
    up: twoD[0].map(letter => colorMap[letter] || "grey"),
    left: twoD[1].map(letter => colorMap[letter] || "grey"),
    front: twoD[2].map(letter => colorMap[letter] || "grey"),
    right: twoD[3].map(letter => colorMap[letter] || "grey"),
    back: twoD[4].map(letter => colorMap[letter] || "grey"),
    down: twoD[5].map(letter => colorMap[letter] || "grey"),
  };
}

// A simple instructions modal
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
        <p>A few things to note about the behaviour of the manual scramble:</p>
        <p>1. The scrambler will not differentiate between capital and lowercase lettering. For example: "R U2 R" will have the same behaviour as "r u2 r". Essentially, there will be no double layered rotations.</p>
        <p>2. The scrambler accepts scrambles separated by a comma and/or a space or neither. For example: "R, U2, R" is the same as "RU2R" as well as "R U2 R".</p>
        <p>3. The scrambler assumes that the input scramble be scrambled under formal WCA regulation. This means that the cube will be scrambled with the white face up, green face forward, and yellow face down etc.</p>
        <p>4. Keep in mind that the actual solution page will denote the solutions with the yellow face up, green face forward, and white face down, as most people using CFOP will solve the cube with a white cross.</p>
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

function Scramble({ onResponse }) {
  const [inputString, setInputString] = useState('');   // State for form input
  const [showInstructions, setShowInstructions] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent page reload

    // Send data to the backend
    fetch('/strsolver', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ body: inputString }), // Send input string as JSON
    })
    .then((res) => res.json())
    .then((data) => {
      // 1) If the backend returns "state" field as 2D array,
      //    convert it to the same format as the camera page uses
      if (data.state && Array.isArray(data.state) && data.state.length === 6) {
        const converted = convert2DToCubeState(data.state);
        
        // 2) Store in localStorage with the same key as the camera page
        localStorage.setItem("lastCubeLayout", JSON.stringify(converted));
      }

      // 3) Let the parent handle the rest of the solution data 
      //    (like cross, f2l, etc.)
      onResponse(data);
    })
    .catch((error) => console.error('Error:', error));
  };

  return (
    <div className="App">
      {/* Instructions Modal */}
      <InstructionsModal
        open={showInstructions}
        onClose={() => setShowInstructions(false)}
      />

      <header className="App-header">
        <h1>Input Your Rubik's Cube Scramble Manually</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Enter Cube String:
            <input
              type="text"
              value={inputString}
              onChange={(e) => setInputString(e.target.value)} // Update state on input change
            />
          </label>
          <button type="submit">Submit</button>
        </form>

        <div style={{ marginTop: "10px" }}>
          <button onClick={() => setShowInstructions(true)}>
            Show Instructions
          </button>
        </div>

        <Link to={`/solver`} style={{ marginTop: "20px" }}>
          View Solution
        </Link>
      </header>
    </div>
  );
}

export default Scramble;
