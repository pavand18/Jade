// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import Ocol from './Ocol';
// import './Input.css'; // Import the existing CSS file

// const Oinput = () => {
//  const [number, setNumber] = useState('');
//  const navigate = useNavigate();
//  const [showPlot, setShowPlot] = useState(false);
//  const [col1Key, setCol1Key] = useState(0);

//  const handleSubmit = async (event) => {
//     event.preventDefault();
//     const response = await fetch('http://localhost:5000/submit5', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ number }),
//     });

//     if (response.ok) {
//       setCol1Key(prevKey => prevKey + 1);
//       setShowPlot(true);
//     } else {
//       alert('Failed to submit number.');
//     }
//  };

//  const calculateCompressionPercentage = async () => {
//   try {
//     const response = await fetch('http://localhost:5000/get-file-sizes');
//     const data = await response.json();

//     if (response.ok) {
//       const inputFileSize = data.inputFileSize;
//       const compressedFilesSizes = Object.values(data.compressedFilesSizes);
//       const totalCompressedSize = compressedFilesSizes.reduce((sum, size) => sum + size, 0);
//       const compressionPercentage = ((inputFileSize - totalCompressedSize) / inputFileSize) * 100;

//       console.log('Input File Size:', inputFileSize);
//       console.log('Compressed Files Sizes:', compressedFilesSizes);
//       console.log(`Compression Percentage: ${compressionPercentage.toFixed(2)}%`);
//     } else {
//       console.error('Failed to calculate compression percentage.');
//     }
//   } catch (error) {
//     console.error('There was a problem calculating compression percentage:', error);
//   }
// };

//  return (
//     <>
//     <div>
//       <form onSubmit={handleSubmit} className="form-container">
//         <input
//           type="number"
//           placeholder="Plot : Column Number"
//           value={number}
//           onChange={(e) => setNumber(e.target.value)}
//           className="input-field"
//         />
//         <button type="submit" className="submit-button">Submit</button>
       
//       </form>
//       <button className="submit-button" onClick={calculateCompressionPercentage}>
//           Compression
//       </button>
//     </div>
//       <div>
//           {showPlot && <Ocol key={col1Key} />}
//       </div>
//     </>
//  );
// };

// export default Oinput;



import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Ocol3 from './Ocol3';
import './Input.css';

const Oinput = () => {
  const [number, setNumber] = useState('');
  const navigate = useNavigate();
  const [showPlot, setShowPlot] = useState(false);
  const [col1Key, setCol1Key] = useState(0);
  const [fileSizeInfo, setFileSizeInfo] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://localhost:5000/submit5', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number }),
    });
    if (response.ok) {
      setCol1Key((prevKey) => prevKey + 1);
      setShowPlot(true);
    } else {
      alert('Failed to submit number.');
    }
  };

  const calculateCompressionPercentage = async () => {
    try {
      const response = await fetch('http://localhost:5000/get-file-sizes3');
      const data = await response.json();
  
      if (response.ok) {
        const inputFileSize = data.inputFileSize / 1024; // Convert to KB
        const compressedFilesSizes = Object.values(data.compressedFilesSizes).map(
          (size) => size / 1024
        ); // Convert to KB
        const totalCompressedSize = compressedFilesSizes.reduce(
          (sum, size) => sum + size,
          0
        );
        const compressionPercentage =
          ((inputFileSize - totalCompressedSize) / inputFileSize) * 100;
  
        const rmseResponse = await fetch('http://localhost:5000/calculate-rmse3');
        const rmseData = await rmseResponse.json();
  
        const info = {
          inputFileSize: inputFileSize.toFixed(2),
          compressedFilesSizes: compressedFilesSizes.map((size) => size.toFixed(2)),
          compressionPercentage: compressionPercentage.toFixed(2),
          rmse: rmseData.rmse,
        };
  
        setFileSizeInfo(info);
      } else {
        console.error('Failed to calculate compression percentage.');
      }
    } catch (error) {
      console.error('There was a problem calculating compression percentage:', error);
    }
  };

  return (
    <>
      <div>
        <form onSubmit={handleSubmit} className="form-container">
          <input
            type="number"
            placeholder="Plot : Column Number"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
            className="input-field"
          />
          <button type="submit" className="submit-button">
            Submit
          </button>
        </form>
        <button className="submit-button" onClick={calculateCompressionPercentage}>
          Compression
        </button>
      </div>
      <div>
        {fileSizeInfo && (
          <div>
            <p>Input File Size: {fileSizeInfo.inputFileSize} KB</p>
            <p>Compressed Files Sizes:</p>
            <ul>
              {fileSizeInfo.compressedFilesSizes.map((size, index) => (
                <li key={index}>File {index + 1}: {size} KB</li>
              ))}
            </ul>
            <p>Compression Percentage: {fileSizeInfo.compressionPercentage}%</p>
            <p>Root Mean Square Error (RMSE): {fileSizeInfo.rmse}</p>
          </div>
        )}
      </div>
      <div>{showPlot && <Ocol3 key={col1Key} />}</div>
    </>
  );
};

export default Oinput;