import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Rcol from './Rcol';

const Rinput = () => {
 const [number, setNumber] = useState('');
 const navigate = useNavigate();
 const [showPlot, setShowPlot] = useState(false);
 // Add a new state to act as a key for Col1
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
      // Increment the col1Key to force a re-render of Col1
      setCol1Key(prevKey => prevKey + 1);
      setShowPlot(true);
    } else {
      alert('Failed to submit number.');
    }
 };

 return (
    <>
      {/* <Linechart /> */}
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Plot : Column Number"
          value={number}
          onChange={(e) => setNumber(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
      <div>
          {showPlot && <Rcol key={col1Key}/>}
      </div>    
    </>
 );
};

export default Rinput;
