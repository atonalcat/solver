import React from "react";
import { Outlet, Link } from "react-router-dom";
import Webcam from "react-webcam";

function Tmp(){

    return (
        <div><li>
            <Webcam
      audio={false}
      height={720}
      screenshotFormat="image/jpeg"
      width={1280}
      // videoConstraints={videoConstraints}
    >
      {({ getScreenshot }) => (
        <button
        onClick={() => {
          const imageSrc = getScreenshot()
          const body = {'body': imageSrc}
          console.log("clicked");
          fetch('/solver',
              {
                  'method':'POST',
                  headers : {'Content-Type':'application/json'},
                  body: JSON.stringify(body)
              }).then(response => console.log(response))
        }}
      >
        Capture photo
      </button>
      )}
    </Webcam>
        <Link to={`/solver`}>Temp Solver Link</Link>
      </li></div>
    );
}
export default Tmp