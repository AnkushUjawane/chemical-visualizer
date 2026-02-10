import { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import Login from './components/Login';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import DatasetHistory from './components/DatasetHistory';
import DatasetDetails from './components/DatasetDetails';
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
      await axios.post(`${API_URL}/login/`, { username, password });
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
      <Login
        username={username}
        password={password}
        setUsername={setUsername}
        setPassword={setPassword}
        onLogin={handleLogin}
        onRegister={handleRegister}
      />
    );
  }

  return (
    <div className="App">
      <Header username={user.username} onLogout={handleLogout} />
      
      <UploadSection 
        onFileChange={(e) => setFile(e.target.files[0])} 
        onUpload={handleUpload} 
      />

      <DatasetHistory 
        datasets={datasets} 
        onView={handleViewDataset} 
        onDownloadPDF={handleDownloadPDF} 
      />

      {selectedDataset && <DatasetDetails dataset={selectedDataset} />}
    </div>
  );
}

export default App;
