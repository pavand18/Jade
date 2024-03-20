// // import React, { useEffect, useState } from 'react';
// // import Plot from 'react-plotly.js';

// // const Ocol = () => {
// //  const [data, setData] = useState([]);
// //  const [val, setVal] = useState([]);

// //  useEffect(() => {
// //     const fetchData = async () => {
// //       const response = await fetch('http://localhost:5000/Ocol');
// //       const result = await response.json();
// //       if (result.success) {
// //         setVal(result.data2);
// //         setData(result.data);
// //       } else {
// //         console.error(result.error);
// //       }
// //     };

// //     fetchData();
// //  }, []);

// //  // Prepare data for the plot
// //  const plotData = [
// //     {
// //       x: Array.from({ length: data.length }, (_, i) => (i + 1) * 0.3),
// //       y: data,
// //       mode: 'lines+markers',
// //       type: 'scatter',
// //       name: 'Fetched Data',
// //       marker: {
// //         color: 'rgb(219, 64, 82)',
// //         size: 1
// //       },
// //       line: {
// //         color: 'rgb(219, 64, 82)',
// //         width: 1
// //       }
// //     }
// //  ];

// //  // Layout options
// //  const layout = {
// //     title: 'Output Data',
// //     xaxis: {
// //       title: 'Time (s)',
// //       showgrid: false,
// //       zeroline: false
// //     },
// //     yaxis: {
// //       title: 'Value',
// //       showline: false
// //     },
// //     autosize: false,
// //     margin: {
// //       autoexpand: false,
// //       l: 100,
// //       r: 20,
// //       t: 110,
// //     },
// //     showlegend: true
// //  };

// //  return (
// //     <Plot
// //       data={plotData}
// //       layout={layout}
// //       config={{
// //         displayModeBar: true,
// //         responsive: true,
// //         scrollZoom: true
// //       }}
// //     />
// //  );
// // };

// // export default Ocol;




// import React, { useEffect, useState } from 'react';
// import Plot from 'react-plotly.js';

// const Ocol = () => {
//  const [data, setData] = useState([]);
//  const [val, setVal] = useState([]);

//  useEffect(() => {
//     const fetchData = async () => {
//       const response = await fetch('http://localhost:5000/Ocol');
//       const result = await response.json();
//       if (result.success) {
//         setVal(result.data2);
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
//       x: Array.from({ length: data.length }, (_, i) => (i + 1) * 0.3),
//       y: data,
//       mode: 'lines+markers',
//       type: 'scatter',
//       name: 'Data',
//       marker: {
//         color: 'rgb(219, 64, 82)',
//         size: 1
//       },
//       line: {
//         color: 'rgb(219, 64, 82)',
//         width: 1
//       }
//     },
//     {
//       x: Array.from({ length: val.length }, (_, i) => (i + 1) * 0.3),
//       y: val,
//       mode: 'lines+markers',
//       type: 'scatter',
//       name: 'Val',
//       marker: {
//         color: 'rgb(85, 219, 82)', // Different color for the second trace
//         size: 1
//       },
//       line: {
//         color: 'rgb(85, 219, 82)', // Different color for the second trace
//         width: 1
//       }
//     }
//  ];

//  // Layout options
//  const layout = {
//     title: 'Output Data',
//     xaxis: {
//       title: 'Time (s)',
//       showgrid: false,
//       zeroline: false
//     },
//     yaxis: {
//       title: 'Value',
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

// export default Ocol;


import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const Ocol = () => {
 const [data, setData] = useState([]);
 const [val, setVal] = useState([]);

 useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/Ocol');
      const result = await response.json();
      if (result.success) {
        setVal(result.data2);
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
      name: 'Data',
      marker: {
        color: 'rgb(219, 64, 82)',
        size: 1
      },
      line: {
        color: 'rgb(219, 64, 82)',
        width: 1
      }
    },
    {
      x: Array.from({ length: val.length }, (_, i) => (i + 1) * 0.3),
      y: val,
      mode: 'lines+markers',
      type: 'scatter',
      name: 'Val',
      marker: {
        color: 'rgb(85, 219, 82)', // Different color for the second trace
        size: 1
      },
      line: {
        color: 'rgb(85, 219, 82)', // Different color for the second trace
        width: 1
      }
    }
 ];

 // Layout options
 const layout = {
    title: 'Output Data',
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

export default Ocol;
