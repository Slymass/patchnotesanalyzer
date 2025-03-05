import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import PatchNotes from "./pages/PatchNotes";

function App() {
  return (
    <Router>
      <div>
        <nav className="p-4 bg-gray-800 text-white flex gap-4">
          <Link to="/">Accueil</Link>
          <Link to="/patch-notes">Patch Notes</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patch-notes" element={<PatchNotes />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
