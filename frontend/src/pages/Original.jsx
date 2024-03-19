import React, { useState, useEffect } from 'react';
import Allsteps from '../components/Allsteps';
import './Original.css'; // Import CSS file for styling
import Oinput from '../components/Oinput';


const Original = () => {
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

  return (
    <div className="original-container">
      <Allsteps />
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
        
      </div>
      <Oinput />
    </div>
 );
};

export default Original;