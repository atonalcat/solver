import react, { useState } from 'react';
import './App.css';
import { Link } from "react-router-dom";

function UserPage() {
    const [input, setInput] = useState("");
  
    const handleClick = () => {
      fetch('/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: input }),
      })
      .then(response => response.json())
      .then(data => {
        // Here you could save the response in the state or in a global state
        // Then you can use it in /solver page
      })
      .catch(error => console.error('Error:', error));
    };
  
    return (
      <div className="App">
        <header className="App-header">
          <input value={input} onChange={e => setInput(e.target.value)} />
          <button onClick={handleClick}>Submit</button>
          <li>
                
          </li>
          <Link to={`/solver`}>Click Here to See Your Solution</Link>
        </header>
      </div>
    );
  }
  export default UserPage;
