import { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const API_URL = 'http://localhost:8000/api';

function App() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [file, setFile] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      fetchDatasets();
    }
  }, []);

  const handleRegister = async () => {
    try {
      await axios.post(`${API_URL}/register/`, { username, password });
      alert('Registration successful! Please login.');
    } catch (error) {
      alert('Registration failed: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${API_URL}/login/`, { username, password });
      const userData = { username, password };
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      fetchDatasets();
    } catch (error) {
      alert('Login failed: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    setDatasets([]);
    setSelectedDataset(null);
  };

  const fetchDatasets = async () => {
    try {
      const response = await axios.get(`${API_URL}/datasets/`, {
        auth: { username: user?.username || username, password: user?.password || password }
      });
      setDatasets(response.data);
    } catch (error) {
      console.error('Failed to fetch datasets:', error);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post(`${API_URL}/upload/`, formData, {
        auth: { username: user.username, password: user.password }
      });
      alert('Upload successful!');
      fetchDatasets();
      setFile(null);
      document.querySelector('input[type="file"]').value = '';
    } catch (error) {
      const errorMsg = error.response?.data?.error || error.message || 'Unknown error';
      alert('Upload failed: ' + errorMsg);
      console.error('Upload error:', error.response?.data);
    }
  };

  const handleViewDataset = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/datasets/${id}/`, {
        auth: { username: user.username, password: user.password }
      });
      setSelectedDataset(response.data);
    } catch (error) {
      alert('Failed to load dataset');
    }
  };

  const handleDownloadPDF = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/datasets/${id}/pdf/`, {
        auth: { username: user.username, password: user.password },
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download PDF');
    }
  };

  if (!user) {
    return (
      <div className="App">
        <h1>Chemical Equipment Visualizer</h1>
        <div className="auth-form">
          <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleRegister}>Register</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header>
        <h1>Chemical Equipment Visualizer</h1>
        <div>
          <span>Welcome, {user.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="upload-section">
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload CSV</button>
      </div>

      <div className="datasets-section">
        <h2>Upload History (Last 5)</h2>
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Upload Date</th>
              <th>Total Count</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {datasets.map((ds) => (
              <tr key={ds.id}>
                <td>{ds.filename}</td>
                <td>{new Date(ds.uploaded_at).toLocaleString()}</td>
                <td>{ds.total_count}</td>
                <td>
                  <button onClick={() => handleViewDataset(ds.id)}>View</button>
                  <button onClick={() => handleDownloadPDF(ds.id)}>PDF</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedDataset && (
        <div className="details-section">
          <h2>Dataset Details: {selectedDataset.filename}</h2>
          
          <div className="summary">
            <h3>Summary Statistics</h3>
            <p>Total Equipment: {selectedDataset.total_count}</p>
            <p>Average Flowrate: {selectedDataset.avg_flowrate.toFixed(2)}</p>
            <p>Average Pressure: {selectedDataset.avg_pressure.toFixed(2)}</p>
            <p>Average Temperature: {selectedDataset.avg_temperature.toFixed(2)}</p>
          </div>

          <div className="charts">
            <div className="chart">
              <h3>Equipment Type Distribution</h3>
              <Pie data={{
                labels: Object.keys(selectedDataset.type_distribution),
                datasets: [{
                  data: Object.values(selectedDataset.type_distribution),
                  backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                }]
              }} />
            </div>

            <div className="chart">
              <h3>Average Parameters</h3>
              <Bar data={{
                labels: ['Flowrate', 'Pressure', 'Temperature'],
                datasets: [{
                  label: 'Average Values',
                  data: [selectedDataset.avg_flowrate, selectedDataset.avg_pressure, selectedDataset.avg_temperature],
                  backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
                }]
              }} />
            </div>
          </div>

          <div className="equipment-table">
            <h3>Equipment List</h3>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                </tr>
              </thead>
              <tbody>
                {selectedDataset.equipment.map((eq, idx) => (
                  <tr key={idx}>
                    <td>{eq.name}</td>
                    <td>{eq.type}</td>
                    <td>{eq.flowrate}</td>
                    <td>{eq.pressure}</td>
                    <td>{eq.temperature}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
