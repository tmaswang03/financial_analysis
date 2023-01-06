
import './App.css'

function App() {
  return (
    <div style = {{ height: "90vh ", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center"}}>
      <h2 style= {{color: "white", fontWeight: "200"}}>Stock Analaysis OBV Indicator</h2>
      <form method = "POST">
        <input type = "text" placeholder = "Enter Stock Here" className = "searchBar"/>
      </form>
    </div>
  );
}

export default App;
