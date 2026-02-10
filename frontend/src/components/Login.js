import React from 'react';

function Login({ username, password, setUsername, setPassword, onLogin, onRegister }) {
  return (
    <div className="App">
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
