// replit

// import React, { useState, useEffect } from 'react';
// import axios from 'axios'; // Import axios
// import Input from '../components/Input';
// import Allsteps from '../components/Allsteps';
// import Plot2 from '../components/Plot2';
// import Plot1 from '../components/Plot1';
// import Plot3 from '../components/Plot3';
// import './Original.css'; // Import CSS file for styling


// const Original = () => {
//   const [csvData, setCsvData] = useState(null);
//   const [csvBlob, setCsvBlob] = useState(null);
//   const [showPlot, setShowPlot] = useState(false);
//   const [comparePlot, setComparePlot] = useState(false);
 
//   const togglePlot = () => {
//    setShowPlot(!showPlot);
//    setComparePlot(false);
//  }; 
 
//  const toggleit = () => {
//    setComparePlot(!comparePlot);
//    setShowPlot(false);
//  };
 
//   useEffect(() => {
//      fetchCsvData();
//   }, []);
 
//   const fetchCsvData = async () => {
//      try {
//        const response = await axios.get('https://a7d966b0-0d45-43cf-ab81-da20ab8751c3-00-5c6bn8ip3ykm.sisko.replit.dev/original', {
//          responseType: 'blob', // Set the response type to blob to handle binary data
//        });
 
//        const blob = new Blob([response.data], { type: 'text/csv' });
//        setCsvBlob(blob);
 
//        // Convert the Blob to text
//        const reader = new FileReader();
//        reader.onload = () => {
//          const text = reader.result;
//          // Parse the CSV text
//          const parsedData = parseCsv(text);
//          setCsvData(parsedData);
//        };
//        reader.readAsText(blob);
//      } catch (error) {
//        console.error('There was a problem with the fetch operation:', error);
//      }
//   };
 
//   const parseCsv = (text) => {
//      const lines = text.split('\n');
//      const headers = lines[0].split(',');
//      const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
//        const values = line.split(',');
//        const row = {};
//        headers.forEach((header, index) => {
//          row[header] = values[index];
//        });
//        return row;
//      });
//      return data;
//   };
 
//   const downloadCsv = () => {
//      if (csvBlob) {
//        const url = window.URL.createObjectURL(csvBlob);
//        const link = document.createElement('a');
//        link.href = url;
//        link.setAttribute('download', 'data.csv');
//        document.body.appendChild(link);
//        link.click();
//        link.parentNode.removeChild(link);
//      }
//   };
 
//   return (
//      <div className="original-container">
//        <Allsteps />
//        {csvData ? (
//          <div>
//            <h2>Output Data:</h2>
//            <table className="data-table">
//              <thead>
//                <tr>
//                  {Object.keys(csvData[0]).map((header, index) => (
//                   <th key={index}>{header}</th>
//                  ))}
//                </tr>
//              </thead>
//              <tbody>
//                {csvData.map((row, rowIndex) => (
//                  <tr key={rowIndex}>
//                   {Object.values(row).map((value, colIndex) => (
//                      <td key={colIndex}>{value}</td>
//                    ))}
//                  </tr>
//                ))}
//              </tbody>
//            </table>
           
//          </div>
//        ) : (
//          <p>Loading CSV data...</p>
//        )}
//        <div>
//          <button className="download-button" onClick={downloadCsv}>Download CSV</button>
//          <button className="data-button" onClick={togglePlot}>
//            {showPlot ? 'Hide Plot' : 'Show Plot'}
//          </button> 
//          <button className="data-button" onClick={toggleit}>
//            {comparePlot ? 'Compare Plot' : 'Compare Plot'}
//          </button>
//        </div>
//        {showPlot && (
//           <div className="plot-container2">
//             <div className="plot">
//               <Plot1 />
//             </div>
//             <div className="plot">
//               <Plot2 />
//             </div>
//           </div>
//         )}
//        {comparePlot && <Plot3 /> }
//      </div>
//   );
//  };
 
//  export default Original;
 



// import React, { useState, useEffect } from 'react';
// import axios from 'axios'; // Import axios
// import Input from '../components/Input';
// import Allsteps from '../components/Allsteps';
// import Plot2 from '../components/Plot2';
// import Plot1 from '../components/Plot1';
// import Plot3 from '../components/Plot3';
// import './Original.css'; // Import CSS file for styling


// const Original = () => {
//   const [csvData, setCsvData] = useState(null);
//   const [csvBlob, setCsvBlob] = useState(null);
//   const [showPlot, setShowPlot] = useState(false);
//   const [comparePlot, setComparePlot] = useState(false);
 
//   const togglePlot = () => {
//    setShowPlot(!showPlot);
//    setComparePlot(false);
//  }; 
 
//  const toggleit = () => {
//    setComparePlot(!comparePlot);
//    setShowPlot(false);
//  };
 
//   useEffect(() => {
//      fetchCsvData();
//   }, []);
 
//   const fetchCsvData = async () => {
//      try {
//        const response = await axios.get('http://localhost:5000/original', {
//          responseType: 'blob', // Set the response type to blob to handle binary data
//        });
 
//        const blob = new Blob([response.data], { type: 'text/csv' });
//        setCsvBlob(blob);
 
//        // Convert the Blob to text
//        const reader = new FileReader();
//        reader.onload = () => {
//          const text = reader.result;
//          // Parse the CSV text
//          const parsedData = parseCsv(text);
//          setCsvData(parsedData);
//        };
//        reader.readAsText(blob);
//      } catch (error) {
//        console.error('There was a problem with the fetch operation:', error);
//      }
//   };
 
//   const parseCsv = (text) => {
//      const lines = text.split('\n');
//      const headers = lines[0].split(',');
//      const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
//        const values = line.split(',');
//        const row = {};
//        headers.forEach((header, index) => {
//          row[header] = values[index];
//        });
//        return row;
//      });
//      return data;
//   };
 
//   const downloadCsv = () => {
//      if (csvBlob) {
//        const url = window.URL.createObjectURL(csvBlob);
//        const link = document.createElement('a');
//        link.href = url;
//        link.setAttribute('download', 'data.csv');
//        document.body.appendChild(link);
//        link.click();
//        link.parentNode.removeChild(link);
//      }
//   };
 
//   return (
//      <div className="original-container">
//        <Allsteps />
//        {csvData ? (
//          <div>
//            <h2>Output Data:</h2>
//            <table className="data-table">
//              <thead>
//                <tr>
//                  {Object.keys(csvData[0]).map((header, index) => (
//                   <th key={index}>{header}</th>
//                  ))}
//                </tr>
//              </thead>
//              <tbody>
//                {csvData.map((row, rowIndex) => (
//                  <tr key={rowIndex}>
//                   {Object.values(row).map((value, colIndex) => (
//                      <td key={colIndex}>{value}</td>
//                    ))}
//                  </tr>
//                ))}
//              </tbody>
//            </table>
           
//          </div>
//        ) : (
//          <p>Loading CSV data...</p>
//        )}
//        <div>
//          <button className="download-button" onClick={downloadCsv}>Download CSV</button>
//          <button className="data-button" onClick={togglePlot}>
//            {showPlot ? 'Hide Plot' : 'Show Plot'}
//          </button> 
//          <button className="data-button" onClick={toggleit}>
//            {comparePlot ? 'Compare Plot' : 'Compare Plot'}
//          </button>
//        </div>
//        {showPlot && (
//           <div className="plot-container2">
//             <div className="plot">
//               <Plot1 />
//             </div>
//             <div className="plot">
//               <Plot2 />
//             </div>
//           </div>
//         )}
//        {comparePlot && <Plot3 /> }
//      </div>
//   );
//  };
 
//  export default Original;
 




import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import axios
import Input from '../components/Input';
import Allsteps from '../components/Allsteps';
import Plot2 from '../components/Plot2';
import Plot1 from '../components/Plot1';
import Plot3 from '../components/Plot3';
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
 
  // const parseCsv = (text) => {
  //    const lines = text.split('\n');
  //    const headers = lines[0].split(',');
  //    const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
  //      const values = line.split(',');
  //      const row = {};
  //      headers.forEach((header, index) => {
  //        row[header] = values[index];
  //      });
  //      return row;
  //    });
  //    return data;
  // };
 
  // const downloadCsv = () => {
  //    if (csvBlob) {
  //      const url = window.URL.createObjectURL(csvBlob);
  //      const link = document.createElement('a');
  //      link.href = url;
  //      link.setAttribute('download', 'data.csv');
  //      document.body.appendChild(link);
  //      link.click();
  //      link.parentNode.removeChild(link);
  //    }
  // };
 

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
        {/* <button className="download-button" onClick={downloadCsv}>Download CSV</button> */}
        {/* <button className="data-button" onClick={togglePlot}>
          {showPlot ? 'Hide Plot' : 'Show Plot'}
        </button> 
        <button className="data-button" onClick={toggleit}>
          {comparePlot ? 'Compare Plot' : 'Compare Plot'}
        </button> */}
      </div>
      {/* {showPlot && (
         <div className="plot-container2">
           <div className="plot">
             <Plot1 />
           </div>
           <div className="plot">
             <Plot2 />
           </div>
         </div>
       )}
      {comparePlot && <Plot3 /> } */}
      <Oinput />
    </div>
 );
};

export default Original;