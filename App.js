import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import "./styles/styles.css";

function App() {
  return (
    <div className="app-container">
      <h1>PDF Image Extractor</h1>
      <FileUpload />
    </div>
  );
}

export default App;
