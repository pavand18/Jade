import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Dcol3 from './Dcol3';
import './Input.css'; // Import the CSS file

const Dinput = () => {
 const [number, setNumber] = useState('');
 const navigate = useNavigate();
 const [showPlot, setShowPlot] = useState(false);
 const [col1Key, setCol1Key] = useState(0);

 const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('http://localhost:5000/submit1', {
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
    <div>
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
      </div>
      <div>
          {showPlot && <Dcol3 key={col1Key} />}
      </div>
    </>
 );
};

export default Dinput;
