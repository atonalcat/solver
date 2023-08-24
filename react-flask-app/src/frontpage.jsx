import React from "react";
import './App.css';
import { Outlet, Link } from "react-router-dom";
function F() {
  return (
    <div className="App">
        <header className="App-header">
            <div> Welcome to the Rubik's Cube Solver. Please click on this button below to continue.</div>
            <nav>
          <ul>
            <li>
              <Link to={`/camera`}>Click Here to Access Camera</Link>
            </li>
            <li>
            <Link to={`/user`}>Click Here to Type Your Scramble</Link>
            </li>
          </ul>
        </nav>
        </header>
    </div>
  );
}

export default F;