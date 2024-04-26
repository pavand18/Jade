import React, { useState, useEffect } from 'react';
import Allsteps4 from '../components/Allsteps4';
import './Reconstruct.css'; // Import CSS file for styling
import Rinput from '../components/Rinput';
import Oinput3 from '../components/Oinput3';


const Reconstruct4 = () => {
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
      const response = await fetch('http://localhost:5000/reconstruct3');
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
      const response = await fetch('http://localhost:5000/download-4');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'Reconstructed_DCT_file.csv');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('There was a problem downloading the file:', error);
    }
  };
 
  return (
     <div className="reconstruct-container">
       <Allsteps4 />
       {csvData ? (
         <div className="data-section">
           <h2>Reconstructed Data:</h2>
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
        {/* <Oinput3 /> */}
      </div>
  );
 };
 
 export default Reconstruct4;