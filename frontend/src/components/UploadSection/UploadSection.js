import React from 'react';
import './UploadSection.css';

function UploadSection({ onFileChange, onUpload }) {
  return (
    <div className="upload-section">
      <input type="file" accept=".csv" onChange={onFileChange} />
      <button onClick={onUpload}>Upload CSV</button>
    </div>
  );
}

export default UploadSection;
