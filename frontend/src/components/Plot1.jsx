import React, { useState, useEffect } from 'react';

const Plot = () => {
 const [plotUrl, setPlotUrl] = useState('');

 useEffect(() => {
    fetchPlot();
 }, []);

 const fetchPlot = async () => {
    try {
      const response = await fetch('http://localhost:5000/plot1');
      const data = await response.json();
      setPlotUrl(data.plot_url);
    } catch (error) {
      console.error('Error fetching plot:', error);
    }
 };

 return (
    <div>
      {plotUrl ? (
        <img src={`data:image/png;base64,${plotUrl}`} alt="Plot" />
      ) : (
        <p>Loading plot...</p>
      )}
    </div>
 );
};

export default Plot;