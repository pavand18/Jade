// original code...

// import React, { useState, useEffect } from 'react';
// import axios from 'axios'; // Import axios
// import Allsteps from '../components/Allsteps';
// import Plot1 from '../components/Plot1';
// import './Data.css'; // Import CSS file for styling

// const Data = () => {
//   const [csvData, setCsvData] = useState(null);
//   const [csvBlob, setCsvBlob] = useState(null);
//   const [showPlot, setShowPlot] = useState(false);

//   const togglePlot = () => {
//     setShowPlot(!showPlot);
//   };

//   useEffect(() => {
//     fetchCsvData();
//   }, []);

//   const fetchCsvData = async () => {
//     try {
//       const response = await axios.get('http://localhost:5000/data', {
//         responseType: 'blob', // Set the response type to blob to handle binary data
//       });

//       const blob = new Blob([response.data], { type: 'text/csv' });
//       setCsvBlob(blob);

//       // Convert the Blob to text
//       const reader = new FileReader();
//       reader.onload = () => {
//         const text = reader.result;
//         // Parse the CSV text
//         const parsedData = parseCsv(text);
//         setCsvData(parsedData);
//       };
//       reader.readAsText(blob);
//     } catch (error) {
//       console.error('There was a problem with the fetch operation:', error);
//     }
//   };

//   const parseCsv = (text) => {
//     const lines = text.split('\n');
//     const headers = lines[0].split(',');
//     const data = lines.slice(1, 5).map((line) => {
//       // Only take the first 4 rows
//       const values = line.split(',');
//       const row = {};
//       headers.forEach((header, index) => {
//         row[header] = values[index];
//       });
//       return row;
//     });
//     return data;
//   };

//   const downloadCsv = () => {
//     if (csvBlob) {
//       const url = window.URL.createObjectURL(csvBlob);
//       const link = document.createElement('a');
//       link.href = url;
//       link.setAttribute('download', 'data.csv');
//       document.body.appendChild(link);
//       link.click();
//       link.parentNode.removeChild(link);
//     }
//   };

//   return (
//     <div className="data-container">
//       <Allsteps />
//       {csvData ? (
//         <div className="data-table-container">
//           <h2 className="data-title">Input Data:</h2>
//           <table className="data-table">
//             <thead>
//               <tr>
//                 {Object.keys(csvData[0]).map((header, index) => (
//                   <th key={index}>{header}</th>
//                 ))}
//               </tr>
//             </thead>
//             <tbody>
//               {csvData.map((row, rowIndex) => (
//                 <tr key={rowIndex}>
//                   {Object.values(row).map((value, colIndex) => (
//                     <td key={colIndex}>{value}</td>
//                   ))}
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       ) : (
//         <p>Loading CSV data...</p>
//       )}
//       <div className="button-container">
//         <button className="data-button" onClick={downloadCsv}>
//               Download CSV
//             </button>
//           <button className="data-button" onClick={togglePlot}>
//           {showPlot ? 'Hide Plot' : 'Show Plot'}
//         </button>
//       </div>
//       {showPlot && <Plot1 />}
//     </div>
//   );
// };

// export default Data;






// import React, { useState, useEffect } from 'react';

// function Data() {
//  const [data, setData] = useState([]);
//  const [loading, setLoading] = useState(true);
//  const [error, setError] = useState(null);

//  useEffect(() => {
//     const fetchData = async () => {

//       try {
//         const response = await fetch('http://localhost:5000/data');
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         const jsonResponse = await response.json();
//         console.log(jsonResponse.data);
//         setData(jsonResponse.data);
//         setLoading(false);
//       } catch (error) {
//         setError(error.message);
//         setLoading(false);
//       }


//     };

//     fetchData();
//  }, []);

//  if (loading) {
//     return <div>Loading...</div>;
//  }

//  if (error) {
//     return <div>Error: {error}</div>;
//  }

//  return (
//     <div>
//       <h1>Data from Flask Backend</h1>
//       <table>
//         <tbody>
//           {data.map((item, rowIndex) => (
//             <tr key={rowIndex}>
//               {Object.values(item).map((value, columnIndex) => (
//                 <td key={columnIndex}>{value}</td>
//               ))}
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//  );
// }

// export default Data;







import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import axios
import Allsteps from '../components/Allsteps';
import Plot1 from '../components/Plot1';
import './Data.css'; // Import CSS file for styling

const Data = () => {
  const [csvData, setCsvData] = useState(null);
  const [csvBlob, setCsvBlob] = useState(null);
  const [showPlot, setShowPlot] = useState(false);

  const togglePlot = () => {
    setShowPlot(!showPlot);
  };

  useEffect(() => {
    fetchCsvData();
  }, []);

  const fetchCsvData = async () => {


    try {
      const response = await fetch('http://localhost:5000/data');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const jsonResponse = await response.json();
      console.log(jsonResponse.data);
      setCsvData(jsonResponse.data);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }


  };

//   const parseCsv = (text) => {
//     const lines = text.split('\n');
//     const headers = lines[0].split(',');
//     const data = lines.slice(1, 5).map((line) => {
//       // Only take the first 4 rows
//       const values = line.split(',');
//       const row = {};
//       headers.forEach((header, index) => {
//         row[header] = values[index];
//       });
//       return row;
//     });
//     return data;
//   };

//   const downloadCsv = () => {
//     if (csvBlob) {
//       const url = window.URL.createObjectURL(csvBlob);
//       const link = document.createElement('a');
//       link.href = url;
//       link.setAttribute('download', 'data.csv');
//       document.body.appendChild(link);
//       link.click();
//       link.parentNode.removeChild(link);
//     }
//   };

  return (
    <div className="data-container">
      <Allsteps />
      {csvData ? (
        <div className="data-table-container">
          <h2 className="data-title">Input Data:</h2>
          <table className="data-table">
            <thead>
              <tr>
                {Object.keys(csvData[0]).map((header, index) => (
                  <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csvData.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {Object.values(row).map((value, colIndex) => (
                    <td key={colIndex}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Loading CSV data...</p>
      )}
      <div className="button-container">
        {/* <button className="data-button" onClick={downloadCsv}>
              Download CSV
            </button> */}
          <button className="data-button" onClick={togglePlot}>
          {showPlot ? 'Hide Plot' : 'Show Plot'}
        </button>
      </div>
      {showPlot && <Plot1 />}
    </div>
  );
};

export default Data;







// import React, { useState, useEffect } from 'react';
// import axios from 'axios'; // Import axios
// import Allsteps from '../components/Allsteps';
// import './Pca.css'; // Import CSS file for styling
// import Plot4 from '../components/Plot4';

// // const Standardise = () => {
// //   const [csvData, setCsvData] = useState(null);
// //   const [csvBlob, setCsvBlob] = useState(null);
// //   const [showPlot, setShowPlot] = useState(false);

// //   const togglePlot = () => {
// //     setShowPlot(!showPlot);
// //   };

// //   useEffect(() => {
// //     fetchCsvData();
// //   }, []);

// //   const fetchCsvData = async () => {


// //     try {
// //         const response = await fetch('http://localhost:5000/dopca');
// //         if (!response.ok) {
// //           throw new Error('Network response was not ok');
// //         }
// //         const jsonResponse = await response.json();
// //         console.log(jsonResponse.data);
// //         setCsvData(jsonResponse.data);
// //         setLoading(false);
// //       } catch (error) {
// //         setError(error.message);
// //         setLoading(false);
// //       }
// //   };

// // //   const parseCsv = (text) => {
// // //     const lines = text.split('\n');
// // //     const headers = lines[0].split(',');
// // //     const data = lines.slice(1, 5).map((line) => {
// // //       // Only take the first 4 rows
// // //       const values = line.split(',');
// // //       const row = {};
// // //       headers.forEach((header, index) => {
// // //         row[header] = values[index];
// // //       });
// // //       return row;
// // //     });
// // //     return data;
// // //   };

// // //   const downloadCsv = () => {
// // //     if (csvBlob) {
// // //       const url = window.URL.createObjectURL(csvBlob);
// // //       const link = document.createElement('a');
// // //       link.href = url;
// // //       link.setAttribute('download', 'data.csv');
// // //       document.body.appendChild(link);
// // //       link.click();
// // //       link.parentNode.removeChild(link);
// // //     }
// // //   };

// return (
//   <div className="pca-container">
//     <Allsteps />
//     {csvData ? (
//       <div className="data-section">
//         <h2>Pca Data:</h2>
//         <table className="data-table">
//           <thead>
//             <tr>
//               {Object.keys(csvData[0]).map((header, index) => (
//                <th key={index}>{header}</th>
//               ))}
//             </tr>
//           </thead>
//           <tbody>
//             {csvData.map((row, rowIndex) => (
//               <tr key={rowIndex}>
//                {Object.values(row).map((value, colIndex) => (
//                   <td key={colIndex}>{value}</td>
//                 ))}
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     ) : (
//       <p>Loading CSV data...</p>
//     )}
//     <div className="button-container">
//         {/* <button className="data-button" onClick={downloadCsv}>
//               Download CSV
//             </button> */}
//           <button className="data-button" onClick={togglePlot}>
//           {showPlot ? 'Hide Plot' : 'Show Plot'}
//         </button>
//       </div>
//       {showPlot && <Plot4 />}
//     </div>
// );
// };

// export default Pca;




