
import React from 'react';
import './App.css'
import {useEffect, useState} from 'react';


function App() {
  const [data, setData] = useState();
  
  const sub = (event) => {
    event.preventDefault()
    var tick = event.target.searchBar.value
    // console.log(tick)
    fetch("/stock/?tick="+tick)
    // fetch("/stock/?tick=" + tick).then( res => {
    //   return res.json()
    // }).then(data => console.log(data))
    return 
  }
  return (
    <div style = {{ height: "90vh ", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center"}}>
      <h2 style= {{color: "white", fontWeight: "200"}}>Stock Analysis OBV Indicator</h2>
      <form action = "/cgi-bin/main.py" method = "get" onSubmit = {sub}>
        <input type = "text" placeholder = "Enter Stock Here" className = "searchBar" name = "searchBar"/>
      </form>
    </div>
  );
}

export default App;
