import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './FileUpload.css'; // Import CSS file for styling

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const onFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const onFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    console.log(file.name);
    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Assuming the backend processes the file and returns a success status
      if (response.data.success) {
        navigate('/dashboard');
      } 
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };


  return (
    <div className="file-upload-container">
      <img className="logo" src="../../public/img/logoo.png" alt="Logo" />
      <h2 className='heading'> PMU DATA <br/> COMPRESSION </h2>
      
      <div className="button-container">
        <div className="button-row1">
          <button className="home-button1" onClick={() => navigate('/upload1')}>PCA Compression</button>
          <button className="home-button1" onClick={() => navigate('/upload2')}>PCA Reconstruction</button>
        </div>
        <div className="button-row2">
          <button className="home-button1" onClick={() => navigate('/upload3')}>DCT Compression</button>
          <button className="home-button1" onClick={() => navigate('/upload4')}>DCT Reconstruction</button>
        </div>
      </div> 
    </div>
  );
};

export default FileUpload;
