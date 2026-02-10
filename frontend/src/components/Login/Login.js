import React from 'react';
import './Login.css';

function Login({ username, password, setUsername, setPassword, onLogin, onRegister }) {
  return (
    <div className="login">
      <h1>Chemical Equipment Visualizer</h1>
      <div className="auth-form">
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button onClick={onLogin}>Login</button>
        <button onClick={onRegister}>Register</button>
      </div>
    </div>
  );
}

export default Login;
