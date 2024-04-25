import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './FileUpload.css'; // Import CSS file for styling

const Upload3 = () => {
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
      const response = await axios.post('http://localhost:5000/upload3', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Assuming the backend processes the file and returns a success status
      if (response.data.success) {
        navigate('/dashboard3');
      } 
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };


  return (
    <div className="file-upload-container">
      <img className="logo" src="../../public/img/logoo.png" alt="Logo" />
      <h2 className='heading'>Data Compression</h2>
      <div className="input-container">
        <input className="upload-input" type="file" onChange={onFileChange} />
        <button className="upload-button" onClick={onFileUpload}>Upload</button>
      </div>
    </div>
  );
};

export default Upload3;
