import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import JSZip from 'jszip';
import './FileUpload.css';

const Upload4 = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const onFileChange = async (event) => {
    const selectedFile = event.target.files[0];
  
    if (selectedFile.type === 'application/zip') {
      try {
        const zipFile = await JSZip.loadAsync(selectedFile);
        const csvFiles = [];
        const csvData = [];
  
        zipFile.forEach((relativePath, zipEntry) => {
          if (zipEntry.name.endsWith('.csv')) {
            csvFiles.push(zipEntry.name); // Store the file name
            csvData.push(zipEntry.async('text')); // Store the CSV data promise
            console.log('Extracted CSV file:', zipEntry.name);
          }
        });
  
        const resolvedData = await Promise.all(csvData);
        console.log('CSV files data:', resolvedData);
        setFile({ names: csvFiles, data: resolvedData });
      } catch (error) {
        console.error('Error extracting CSV files:', error);
      }
    } else {
      console.error('Please select a ZIP file containing CSV files.');
    }
  };    

  const onFileUpload = async () => {
    if (file && file.data && file.names) {
      const formData = new FormData();
  
      file.data.forEach((csvData, index) => {
        const csvBlob = new Blob([csvData], { type: 'text/csv' });
        formData.append('files', csvBlob, file.names[index]);
      });
  
      try {
        const response = await axios.post('http://localhost:5000/upload4', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        // Assuming the backend processes the files and returns a success status
        if (response.data.success) {
          navigate('/dashboard4');
        }
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    } else {
      console.error('No CSV files selected.');
    }
  };    

  return (
    <div className="file-upload-container">
      <img className="logo" src="../../public/img/logoo.png" alt="Logo" />
      <h2 className="heading">DCT Reconstruction</h2>
      <div className="input-container">
        <input
          className="upload-input"
          type="file"
          accept=".zip"
          onChange={onFileChange}
        />
        <button className="upload-button" onClick={onFileUpload}>
          Upload
        </button>
      </div>
    </div>
  );
};

export default Upload4;