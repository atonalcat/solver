import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Frontpage from './frontpage';
import Camera from './camerapage';
import Tmp from './tmp';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
const router = createBrowserRouter([
  {
    path: "/",
    element: <Frontpage />,
  }, 
  {
    path: "/camera",
    element: <Camera />,
  },
  {
    path: "/solver",
    element: <App />,
  }
]);
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
