import React from 'react';
import { NavLink } from "react-router-dom";
import "./Allsteps.css"; // Import CSS file for styling

function Allsteps3() {
    return (
        <div className="all-steps-container">
            <ul className="steps-list">
                <li>
                    <NavLink to="/dashboard3/data3" className="step-button" activeClassName="active">Input</NavLink>
                </li>
                {/* <li>
                    <NavLink to="/dashboard/standardise" className="step-button" activeClassName="active">Standardise</NavLink>
                </li> */}
                {/* <li>
                    <NavLink to="/dashboard/submit" className="step-button" activeClassName="active">PCA</NavLink>
                </li> */}
                <li>
                    <NavLink to="/dashboard3/compress3" className="step-button" activeClassName="active">Compression</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard3/reconstruct3" className="step-button" activeClassName="active">Reconstruction</NavLink>
                </li>
            </ul>
        </div>
    );
}

export default Allsteps3;