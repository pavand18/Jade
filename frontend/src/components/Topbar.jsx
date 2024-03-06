import React from 'react';
import { Link } from 'react-router-dom';
import './Topbar.css';

const Topbar = () => {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <button class="btn"><i class="fa fa-home"></i></button>
        {/* <button className="home-button">Home</button> */}
      </Link>
      <span className="brand-name">Big Sync</span>
      <Link to="/" >
        <button className="upload-file-button">Upload File</button>
      </Link>
    </nav>
  );
};

export default Topbar;
