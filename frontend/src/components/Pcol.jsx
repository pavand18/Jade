// import React, { useEffect, useState } from 'react';
// import Plot from 'react-plotly.js';

// const Pcol = () => {
//  const [data, setData] = useState([]);

//  useEffect(() => {
//     const fetchData = async () => {
//       const response = await fetch('http://localhost:5000/var');
//       const result = await response.json();
//       if (result.success) {
//         setData(result.data);
//       } else {
//         console.error(result.error);
//       }
//     };

//     fetchData();
//  }, []);

//  // Prepare data for the plot
//  const plotData = [
//     {
//       x: Array.from({ length: data.length }, (_, i) => i + 1),
//       y: data,
//       mode: 'lines+markers',
//       type: 'scatter',
//       name: 'Fetched Data',
//       marker: {
//         color: 'rgb(219, 64, 82)',
//         size: 5
//       },
//       line: {
//         color: 'rgb(219, 64, 82)',
//         width: 1
//       }
//     }
//  ];

//  // Layout options
//  const layout = {
//     title: 'Pc Variance',         
//     xaxis: {
//       title: 'Pc',
//       showgrid: false,
//       zeroline: false
//     },
//     yaxis: {
//       title: 'Variance',
//       showline: false
//     },
//     autosize: false,
//     margin: {
//       autoexpand: false,
//       l: 100,
//       r: 20,
//       t: 110,
//     },
//     showlegend: true
//  };

//  return (
//     <Plot
//       data={plotData}
//       layout={layout}
//       config={{
//         displayModeBar: true,
//         responsive: true,
//         scrollZoom: true
//       }}
//     />
//  );
// };

// export default Pcol;


import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const Pcol = () => {
 const [data, setData] = useState([]);

 useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/var');
      const result = await response.json();
      if (result.success) {
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
      x: Array.from({ length: data.length }, (_, i) => i + 1),
      y: data,
      mode: 'lines+markers',
      type: 'scatter',
      name: 'Fetched Data',
      marker: {
        color: 'rgb(219, 64, 82)',
        size: 5
      },
      line: {
        color: 'rgb(219, 64, 82)',
        width: 1
      }
    }
 ];

 // Layout options
 const layout = {
    title: 'Pc Variance',         
    xaxis: {
      title: 'Pc',
      showgrid: false,
      zeroline: false
    },
    yaxis: {
      title: 'Variance',
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
    // border: '1px solid #ccc', // Light border
    padding: '20px', // Padding inside the border
    margin: '20px auto', // Centering the container
    maxWidth: '80%', // Optional: limit the maximum width
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

export default Pcol;
