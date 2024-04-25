import React, { useState, useEffect } from 'react';
import Allsteps3 from '../components/Allsteps3';
import './Standardise.css'; // Import CSS file for styling
import Sinput from '../components/Sinput';


const Compress = () => {
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
        const response = await fetch('http://localhost:5000/compress3');
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

  const handleDownloadFiles = async () => {
    try {
      const response = await fetch('http://localhost:5000/download-files3');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'dct_compressed_files.zip');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('There was a problem downloading the files:', error);
    }
  };

return (
  <div className="standardise-container">
    <Allsteps3 />
    {/* <LineChart /> */}
    {csvData ? (
      <div className="data-section" >
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
      </div>
    ) : (
      <p>Loading CSV data...</p>
    )}
    <div className="button-container">
        <button className="data-button" onClick={handleDownloadFiles}>
          Download Compressed Files (2)
        </button> 
    </div>
      {/* <Sinput /> */}
    </div>
);
};

export default Compress;

