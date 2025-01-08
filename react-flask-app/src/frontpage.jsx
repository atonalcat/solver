import React, { useState } from "react";
import './App.css';
import { Outlet, Link } from "react-router-dom";

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
          {/* Replace this placeholder text with your own instructions */}
          This application allows you to solve a Rubik's Cube in two ways:
          <br /><br />
          1. Use your device’s camera to capture each face of the cube (or manually inputting the colors of each face if camera access is unavailable).<br/>
          2. Manually enter the scramble (or known state) of your cube.<br/><br/>
          There are much more efficient and short algorithms out there compared to the ones used by this application, but the intent of this project is not to achieve the minimum moves (which is either 20 or less) possible in a solution. This application is designed for beginner to rookie cubers who are trying or just beginning to understand the concepts of CFOP.
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

function F() {
  const [showInstructions, setShowInstructions] = useState(false);

  return (
    <div className="App">
      <InstructionsModal
        open={showInstructions}
        onClose={() => setShowInstructions(false)}
      />

      <header className="App-header">
        <div> 
          Welcome to the Rubik's Cube Solver. Please click on the following options below to continue.
        </div>

        <nav>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li style={{ margin: "10px 0" }}>
              <Link to={`/camera`}>Click Here to Access Camera</Link>
            </li>
            <li style={{ margin: "10px 0" }}>
              <Link to={`/inputscramble`}>Click Here to Input Your Rubik's Cube Scramble Manually</Link>
            </li>
          </ul>
        </nav>

        <button 
          onClick={() => setShowInstructions(true)}
          style={{ marginTop: "15px", padding: "8px 16px", cursor: "pointer" }}
        >
          Show Instructions
        </button>
      </header>
    </div>
  );
}

export default F;
