// src/FileUpload.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

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
    <div>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>
    </div>
 );
};

export default FileUpload;
