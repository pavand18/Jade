import React, { useState, useEffect } from 'react';
import './Plot.css'; // 

const Plot = () => {
 const [plotUrl, setPlotUrl] = useState('');

 useEffect(() => {
    fetchPlot();
 }, []);

 const fetchPlot = async () => {
    try {
      const response = await fetch('https://a7d966b0-0d45-43cf-ab81-da20ab8751c3-00-5c6bn8ip3ykm.sisko.replit.dev/plot4');
      const data = await response.json();
      setPlotUrl(data.plot_url);
    } catch (error) {
      console.error('Error fetching plot:', error);
    }
 };

 return (
    <div className="plot-container">
      {plotUrl ? (
        <img className="plot-image" src={`data:image/png;base64,${plotUrl}`} alt="Plot" />
      ) : (
        <p>Loading plot...</p>
      )}
    </div>
 );
};

export default Plot;