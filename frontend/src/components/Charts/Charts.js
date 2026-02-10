import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import './Charts.css';

function Charts({ dataset }) {
  return (
    <div className="charts">
      <div className="chart">
        <h3>Equipment Type Distribution</h3>
        <Pie data={{
          labels: Object.keys(dataset.type_distribution),
          datasets: [{
            data: Object.values(dataset.type_distribution),
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
            data: [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature],
            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
          }]
        }} />
      </div>
    </div>
  );
}

export default Charts;
