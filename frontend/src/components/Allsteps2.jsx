import React from 'react';
import { NavLink } from "react-router-dom";
import "./Allsteps.css"; // Import CSS file for styling

function Allsteps2() {
    return (
        <div className="all-steps-container">
            <ul className="steps-list">
                <li>
                    <NavLink to="/dashboard2/data2" className="step-button" activeClassName="active">Input</NavLink>
                </li>
                {/* <li>
                    <NavLink to="/dashboard/standardise" className="step-button" activeClassName="active">Standardise</NavLink>
                </li> */}
                {/* <li>
                    <NavLink to="/dashboard/submit" className="step-button" activeClassName="active">PCA</NavLink>
                </li> */}
                <li>
                    <NavLink to="/dashboard2/reconstruct2" className="step-button" activeClassName="active">Reconstruct</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard2/original2" className="step-button" activeClassName="active">Output</NavLink>
                </li>
            </ul>
        </div>
    );
}

export default Allsteps2;



