import React, { useState, useEffect } from 'react';
import Allsteps3 from '../components/Allsteps3';
import './Data.css'; // Import CSS file for styling
import Dinput3 from '../components/Dinput3';


const Data3 = () => {
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
      const response = await fetch('http://localhost:5000/data3');
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
    <div className="data-container">
      <Allsteps3 />
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
      {/* <div className="button-container">
        
      </div> */}
      <Dinput3 />
    </div>
  );
};

export default Data3;