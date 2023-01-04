import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import { Outlet, Link } from "react-router-dom";


const body = {'body': "brawlstars"}
function App() {
  const [cross, setCross] = useState(0);
  const [first, setFirst] = useState(0);
  const [FTL, setF2L] = useState(0);
  const [OLL, setOLL] = useState(0);
  const [PLL, setPLL] = useState(0);
  const [AUF, setAUF] = useState(0);
  const [scramble, setScramble] = useState(0);
  const [CS, setCS] = useState(0);


  useEffect(() => {
    fetch('/solver',{
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify(body)
    }).then(res => res.json()).then(data => {
      setCross(data.cross);
      setFirst(data.first)
      setF2L(data.ftl)
      setOLL(data.oll)
      setPLL(data.pll)
      setAUF(data.auf)
      setScramble(data.scramble)
      setCS(data.cubestate)
      console.log("sfasf")
      console.log(data.cross)
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">


        <h>The solution is (instructions based with green face in front, yellow face on top, and white on bottom): </h>
        <p>White Cross: {cross}</p>
        <p>White Face: {first}</p>
        <p>F2L: {FTL}</p>
        <p>OLL: {OLL}</p>
        <p>PLL: {PLL}</p>
        <p>AUF: {AUF}</p>
        <p>SCRAMBLE: {scramble}</p>
        <p>cubeState: {CS}</p>
        <Link to={`/`}>Click Here to Go Back to Homepage</Link>
      </header>
    </div>
  );
}

export default App;