import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Rcol from './Rcol';
import './Input.css'; // Import the existing CSS file

const Rinput = () => {
 const [number, setNumber] = useState('');
 const navigate = useNavigate();
 const [showPlot, setShowPlot] = useState(false);
 const [col1Key, setCol1Key] = useState(0);

 const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://localhost:5000/submit4', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number }),
    });

    if (response.ok) {
      setCol1Key(prevKey => prevKey + 1);
      setShowPlot(true);
    } else {
      alert('Failed to submit number.');
    }
 };

 return (
    <>
      <form onSubmit={handleSubmit} className="form-container">
        <input
          type="number"
          placeholder="Plot : Column Number"
          value={number}
          onChange={(e) => setNumber(e.target.value)}
          className="input-field"
        />
        <button type="submit" className="submit-button">Submit</button>
      </form>
      <div>
          {showPlot && <Rcol key={col1Key} />}
      </div>
    </>
 );
};

export default Rinput;

