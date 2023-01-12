
import React from 'react';
import './App.css'
import {useEffect, useState} from 'react';
import Plot from 'react-plotly.js';


function App() {
  const [OBV, setOBV] = useState();
  const[graph, setGraph] = useState(0);
  
  const sub = (event) => {
    event.preventDefault()
    var tick = event.target.searchBar.value
    fetch("/stock/?tick=" + tick).then( res => {
      return res.json()
    }).then(data => {
      console.log(data)
      setGraph(JSON.parse(data["graph"]))
      setOBV(data["OBV"])
      console.log(graph)
      // graph.layout["plot_bgcolor"] = "black"
      // graph.layout.bgcolor = "black"
    })
    return 
  }
  return (
    <div style = {{ height: "90vh ", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center"}}>
      <h2 style= {{color: "white", fontWeight: "200"}}>Stock Analysis OBV Indicator</h2>
      <form action = "/cgi-bin/main.py" method = "get" onSubmit = {sub}>
        <input type = "text" placeholder = "Enter Stock Here" className = "searchBar" name = "searchBar"/>
      </form> 
      {/* <{graph ? <Plot data = {graph.data} layout = {graph.layout}/> : null}> */}
      {graph ? <Plot style = {{ margin: "1em"}} data = {graph.data} layout = {graph.layout} /> : null}
    </div>
  );
}

export default App;
