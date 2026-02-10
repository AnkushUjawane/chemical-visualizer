import React from 'react';

function Header({ username, onLogout }) {
  return (
    <header>
      <h1>Chemical Equipment Visualizer</h1>
      <div>
        <span>Welcome, {username}</span>
        <button onClick={onLogout}>Logout</button>
      </div>
    </header>
  );
}

export default Header;
