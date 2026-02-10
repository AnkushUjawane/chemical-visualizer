import React from 'react';
import Charts from './Charts';

function DatasetDetails({ dataset }) {
  return (
    <div className="details-section">
      <h2>Dataset Details: {dataset.filename}</h2>
      
      <div className="summary">
        <h3>Summary Statistics</h3>
        <p>Total Equipment: {dataset.total_count}</p>
        <p>Average Flowrate: {dataset.avg_flowrate.toFixed(2)}</p>
        <p>Average Pressure: {dataset.avg_pressure.toFixed(2)}</p>
        <p>Average Temperature: {dataset.avg_temperature.toFixed(2)}</p>
      </div>

      <Charts dataset={dataset} />

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
            {dataset.equipment.map((eq, idx) => (
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
  );
}

export default DatasetDetails;
