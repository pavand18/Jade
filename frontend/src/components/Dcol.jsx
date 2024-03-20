import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const Dcol = () => {
 const [data, setData] = useState([]);

 useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/col1');
      const result = await response.json();
      if (result.success) {
        console.log(result.data2);
        setData(result.data);
      } else {
        console.error(result.error);
      }
    };

    fetchData();
 }, []);

 // Prepare data for the plot
 const plotData = [
    {
      x: Array.from({ length: data.length }, (_, i) => (i + 1) * 0.3),
      y: data,
      mode: 'lines+markers',
      type: 'scatter',
      name: 'Fetched Data',
      marker: {
        color: 'rgb(219, 64, 82)',
        size: 1
      },
      line: {
        color: 'rgb(219, 64, 82)',
        width: 1
      }
    }
 ];

 // Layout options
 const layout = {
    title: 'Input Plot',
    xaxis: {
      title: 'Time (s)',
      showgrid: false,
      zeroline: false
    },    
    yaxis: {
      title: 'Value',
      showline: false
    },
    autosize: false,
    margin: {
      autoexpand: false,
      l: 100,
      r: 20,
      t: 110,
    },
    showlegend: true
 };

 // Inline styles for centering and adding a light border
 const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    // border: '1px solid darkblue', // Light border
    padding: '20px', // Padding inside the border
    margin: '20px auto', // Centering the container
    maxWidth: '50%', // Optional: limit the maximum width
 };

 return (
    <div style={containerStyle}>
      <Plot
        data={plotData}
        layout={layout}
        config={{
          displayModeBar: true,
          responsive: true,
          scrollZoom: true
        }}
      />
    </div>
 );
};

export default Dcol;
