import React from "react";
import Chat from "./components/Chat";

function App() {
  return (
    <div className="app-root">
      <div className="app-gradient" />
      <div className="app-container">
        <header className="app-header">
          <div className="logo-circle">M</div>
          <div>
            <h1 className="app-title">MindEase Companion</h1>
            <p className="app-subtitle">
              A gentle AI space for reducing loneliness and supporting your emotions.
            </p>
          </div>
        </header>
        <Chat />
      </div>
    </div>
  );
}

export default App;
