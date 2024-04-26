import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Allsteps2 from '../components/Allsteps2';

const Data2 = () => {
  const [fileInfo, setFileInfo] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFileInfo = async () => {
      try {
        const response = await axios.get('http://localhost:5000/data2');
        if (response.data.success) {
          setFileInfo(response.data.files);
        } else {
          setError(response.data.error);
        }
      } catch (error) {
        setError('An error occurred while fetching file information.');
      }
    };

    fetchFileInfo();
  }, []);

  const formatSize = (size) => {
    return (size / 1024).toFixed(2) + ' KB';
  };

  return (
    <div>
        <Allsteps2 />
        <h2>Input Files Information</h2>
        {error && <p>{error}</p>}
        {fileInfo.length === 0 ? (
            <p>No file information available.</p>
        ) : (
            <ul>
            {fileInfo.map((file, index) => (
                <li key={index}>
                <p>
                    {file.name} :- {formatSize(file.size)}
                </p>
                </li>
            ))}
            </ul>
        )}
        </div>
    );
};

export default Data2;