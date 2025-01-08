import React, { useState, useEffect } from 'react';
import App from "./App.jsx";
import Scramble from "./scramble.jsx";

function ParentComponent() {
    const [response, setResponse] = useState(null);
    useEffect(() => {
        if (response) {
          localStorage.setItem("response", JSON.stringify(response));
        }
    }, [response]);
    return (
      <div>
        {/* FormComponent sends the response data to the parent */}
        <Scramble onResponse={setResponse} />
      </div>
    );
  }
  
  export default ParentComponent;
