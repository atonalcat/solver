import React, { useState, useEffect } from 'react';
import './App.css';
import { Link } from "react-router-dom";

// We'll reuse a Face component to display a 3×3 face read-only.
function getSquareStyle(color) {
  return {
    width: "20px", // smaller squares to keep the net compact
    height: "20px",
    backgroundColor: color,
    border: "1px solid #222",
    boxSizing: "border-box",
    // read-only, so no cursor pointer needed
  };
}

function ReadOnlyFace({ squares }) {
  return (
    <div 
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 20px)",
        margin: "2px" // tight spacing
      }}
    >
      {squares.map((color, idx) => (
        <div key={idx} style={getSquareStyle(color)} />
      ))}
    </div>
  );
}

function CubeNet({ layout }) {
  // layout: { up, left, front, right, back, down }
  // Each is an array of 9 colors

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      {/* Up face */}
      <ReadOnlyFace squares={layout.up} />

      {/* Middle row: left, front, right, back */}
      <div style={{ display: "flex" }}>
        <ReadOnlyFace squares={layout.left} />
        <ReadOnlyFace squares={layout.front} />
        <ReadOnlyFace squares={layout.right} />
        <ReadOnlyFace squares={layout.back} />
      </div>

      {/* Down face */}
      <ReadOnlyFace squares={layout.down} />
    </div>
  );
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
        zIndex: 9999
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
        <p>
          {/* Replace this text with your real instructions */}
          This page shows the final solution to your Rubik's Cube. <br></br>
          The net in the bottom-right corner displays your last captured layout.
          <br></br><br></br>
          Keep in mind of the following:<br></br>
          1. If you input your scramble via the text form, it will automatically be translated with respect to the yellow face up, green face front, and white face bottom layout.<br></br>
          2. If the cube state shows invalid, that means that your input scramble contained non standard terms for cube moves. Refer to the manual scramble page for more information.<br></br>
          3. If the cube state shows unsolvable, that means that you have input some information incorrectly via the visual section (and/or your cube may have a corner twist)
        </p>

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

function App() {
  const [cross, setCross] = useState(0);
  const [first, setFirst] = useState(0);
  const [FTL, setF2L] = useState(0);
  const [OLL, setOLL] = useState(0);
  const [PLL, setPLL] = useState(0);
  const [AUF, setAUF] = useState(0);
  const [scramble, setScramble] = useState(0);
  const [CS, setCS] = useState(0);

  // We'll store the lastCubeLayout in state as well
  const [lastLayout, setLastLayout] = useState(null);

  // For instructions modal
  const [showInstructions, setShowInstructions] = useState(false);

  let response = null;

  useEffect(() => {
    // 1) Load the solution data from localStorage
    const storedResponse = localStorage.getItem("response");
    if (storedResponse) {
      response = JSON.parse(storedResponse);
      if (response && response.valid) {
        setCross(response.cross);
        setFirst(response.first);
        setF2L(response.ftl);
        setOLL(response.oll);
        setPLL(response.pll);
        setAUF(response.auf);
        setScramble(response.scramble);
        setCS(response.cubestate);
        console.log("Response processed.");
      } else {
        setCS(response?.error || "No valid solution found");
      }
    }

    // 2) Load the last saved cube layout from localStorage
    const storedLayout = localStorage.getItem("lastCubeLayout");
    if (storedLayout) {
      const parsedLayout = JSON.parse(storedLayout);
      setLastLayout(parsedLayout);
    }
  }, [response]);

  return (
    <div className="App">
      {/* Instructions Modal */}
      <InstructionsModal
        open={showInstructions}
        onClose={() => setShowInstructions(false)}
      />

      <header className="App-header">
        <h>
          The solution is (instructions based with green face in front, 
          yellow face on top, and white on bottom):
        </h>
        <p>White Cross: {cross}</p>
        <p>White Face: {first}</p>
        <p>F2L: {FTL}</p>
        <p>OLL: {OLL}</p>
        <p>PLL: {PLL}</p>
        <p>AUF: {AUF}</p>
        <p>SCRAMBLE: {scramble}</p>
        <p>cubeState: {CS}</p>

        <div style={{ marginBottom: "10px" }}>
          <button 
            onClick={() => setShowInstructions(true)}
            style={{ padding: "8px 16px", cursor: "pointer" }}
          >
            Show Instructions
          </button>
        </div>

        <Link to={`/`}>Click Here to Go Back to Homepage</Link>
      </header>

      {/* If we have a lastLayout, render a small cube net at bottom-right */}
      {lastLayout && (
        <div
          style={{
            position: "absolute",
            bottom: "20px",
            right: "20px",
            backgroundColor: "white",
            border: "1px solid #ccc",
            borderRadius: "6px",
            padding: "10px"
          }}
        >
          <h4 style={{ margin: "0 0 5px 0", fontSize: "14px" }}>Last Cube Layout</h4>
          <CubeNet layout={lastLayout} />
        </div>
      )}
    </div>
  );
}

export default App;
