// src/Input.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Input = () => {
 const navigate = useNavigate();

 const handleClick = () => {
    navigate('/');
 };

 return (
    <div>
      <button onClick={handleClick}>Go to Dashboard</button>
    </div>
 );
};

export default Input;
