import React from 'react';
import './DatasetHistory.css';

function DatasetHistory({ datasets, onView, onDownloadPDF }) {
  return (
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
                <button onClick={() => onView(ds.id)}>View</button>
                <button onClick={() => onDownloadPDF(ds.id)}>PDF</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DatasetHistory;
