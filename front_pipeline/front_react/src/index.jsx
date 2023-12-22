import React from "react";
import ReactDOM from "react-dom";


const App = () => {
  return <div><h1>Hello World</h1></div>;
};

const root_id = "spa-react"

ReactDOM.render(
  <App />,
  document.getElementById(root_id)
);
