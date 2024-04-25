import React, { useState, useEffect } from 'react';
import Allsteps2 from '../components/Allsteps2';
import './Original.css'; // Import CSS file for styling
import Oinput from '../components/Oinput';


const Original2 = () => {
  const [csvData, setCsvData] = useState(null);
  const [csvBlob, setCsvBlob] = useState(null);
  const [showPlot, setShowPlot] = useState(false);
  const [comparePlot, setComparePlot] = useState(false);
  
 
  const togglePlot = () => {
    setShowPlot(!showPlot);
    setComparePlot(false);
  }; 
  
  const toggleit = () => {
    setComparePlot(!comparePlot);
    setShowPlot(false);
  };
 
  useEffect(() => {
     fetchCsvData();
  }, []);
 
  const fetchCsvData = async () => {

    try {
      const response = await fetch('http://localhost:5000/original');
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

//   const handleDownloadFile = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/download-file');
//       const blob = await response.blob();
//       const downloadUrl = window.URL.createObjectURL(blob);
//       const link = document.createElement('a');
//       link.href = downloadUrl;
//       link.setAttribute('download', 'Reconstructed_data.csv');
//       document.body.appendChild(link);
//       link.click();
//       link.parentNode.removeChild(link);
//     } catch (error) {
//       console.error('There was a problem downloading the file:', error);
//     }
//   };

const handleDownloadFiles = async () => {
    try {
      const response = await fetch('http://localhost:5000/download-compressed-csv');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'Reconstructed_file.csv');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('There was a problem downloading the file:', error);
    }
  };

  return (
    <div className="original-container">
      <Allsteps2 />
      {csvData ? (
        <div>
          <h2>Output Data:</h2>
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
      <div>
        <button className="data-button" onClick={handleDownloadFiles}>
            Download files
        </button>                                  
      </div>
    </div>
 );
};

export default Original2;