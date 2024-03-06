// import React, { useState, useEffect } from 'react';
// import axios from 'axios'; // Import axios
// import Input from '../components/Input';
// import Allsteps from '../components/Allsteps';

// const Standardise = () => {
//  const [csvData, setCsvData] = useState(null);
//  const [csvBlob, setCsvBlob] = useState(null);

//  useEffect(() => {
//     fetchCsvData();
//  }, []);

//  const fetchCsvData = async () => {
//     try {
//       const response = await axios.get('http://localhost:5000/standardise', {
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
//  };

//  const parseCsv = (text) => {
//     const lines = text.split('\n');
//     const headers = lines[0].split(',');
//     const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
//       const values = line.split(',');
//       const row = {};
//       headers.forEach((header, index) => {
//         row[header] = values[index];
//       });
//       return row;
//     });
//     return data;
//  };

//  const downloadCsv = () => {
//     if (csvBlob) {
//       const url = window.URL.createObjectURL(csvBlob);
//       const link = document.createElement('a');
//       link.href = url;
//       link.setAttribute('download', 'data.csv');
//       document.body.appendChild(link);
//       link.click();
//       link.parentNode.removeChild(link);
//     }
//  };

//  return (
//     <div>
//       <Input />
//       <Allsteps />
//       {csvData ? (
//         <div>
//           <h2>Standardise Data:</h2>
//           <table>
//             <thead>
//               <tr>
//                 {Object.keys(csvData[0]).map((header, index) => (
//                  <th key={index}>{header}</th>
//                 ))}
//               </tr>
//             </thead>
//             <tbody>
//               {csvData.map((row, rowIndex) => (
//                 <tr key={rowIndex}>
//                  {Object.values(row).map((value, colIndex) => (
//                     <td key={colIndex}>{value}</td>
//                   ))}
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//           <button onClick={downloadCsv}>Download CSV</button>
//         </div>
//       ) : (
//         <p>Loading CSV data...</p>
//       )}
//     </div>
//  );
// };

// export default Standardise;


import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import axios
import Input from '../components/Input';
import Allsteps from '../components/Allsteps';
import './Standardise.css'; // Import CSS file for styling

const Standardise = () => {
 const [csvData, setCsvData] = useState(null);
 const [csvBlob, setCsvBlob] = useState(null);

 useEffect(() => {
    fetchCsvData();
 }, []);

 const fetchCsvData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/standardise', {
        responseType: 'blob', // Set the response type to blob to handle binary data
      });

      const blob = new Blob([response.data], { type: 'text/csv' });
      setCsvBlob(blob);

      // Convert the Blob to text
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        // Parse the CSV text
        const parsedData = parseCsv(text);
        setCsvData(parsedData);
      };
      reader.readAsText(blob);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
 };

 const parseCsv = (text) => {
    const lines = text.split('\n');
    const headers = lines[0].split(',');
    const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
      const values = line.split(',');
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index];
      });
      return row;
    });
    return data;
 };

 const downloadCsv = () => {
    if (csvBlob) {
      const url = window.URL.createObjectURL(csvBlob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'data.csv');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    }
 };

 return (
    <div className="standardise-container">
      <Allsteps />
      {csvData ? (
        <div className="data-section">
          <h2>Standardise Data:</h2>
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
          <button className="download-button" onClick={downloadCsv}>Download CSV</button>
        </div>
      ) : (
        <p>Loading CSV data...</p>
      )}
    </div>
 );
};

export default Standardise;
