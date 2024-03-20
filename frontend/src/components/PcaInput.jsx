import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Allsteps from './Allsteps';
import Pca from '../pages/Pca';
import './Input.css'; // Import the CSS file

const PcaInput = () => {
 const [number, setNumber] = useState('');
 const navigate = useNavigate();
 const [showPlot, setShowPlot] = useState(false);
 const [col1Key, setCol1Key] = useState(0);

 const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://localhost:5000/submit3', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number }),
    });

    if (response.ok) {
      // navigate('/dashboard/pca');
      setCol1Key(prevKey => prevKey + 1);
      setShowPlot(true);
    } else {
      alert('Failed to submit number.');
    }
 };

 return (
    <>
        {/* <Linechart /> */}
        <Allsteps />
        <form onSubmit={handleSubmit} className="form-container">
        <input
            type="number"
            placeholder="Number of PC"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
            className="input-field"
        />
        <button type="submit" className="submit-button">Submit</button>
        </form>
        <div>
          {showPlot && <Pca key={col1Key} />}
        </div>
    </>
 );
};

export default PcaInput;



