import React, { useState, useEffect } from 'react';
import './Pca.css'; // Import CSS file for styling
import Pcol from '../components/Pcol';


const Pca = () => {
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
        const response = await fetch('http://localhost:5000/dopca');
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

return (
  <div className="pca-container">
    {/* <Allsteps /> */}
    {/* <NumberInputForm /> */}
    {csvData ? (
      <div className="data-section">
        <h2>Pca Data:</h2>
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
          <button className="data-button" onClick={togglePlot}>
          {showPlot ? 'Hide Plot' : 'Show Plot'}
        </button>
      </div>
      {showPlot && <Pcol />}
    </div>
);
};

export default Pca;

