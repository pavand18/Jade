import React from 'react';
import { NavLink } from "react-router-dom";

function Allsteps () {
    return (
        <>
        <ul>
            <li>
            <NavLink to="/dashboard/data"> Data </NavLink>
            </li>
            <li>
            <NavLink to="/dashboard/standardise"> standardise </NavLink>
            </li>
            <li>
            <NavLink to="/dashboard/pca"> pca </NavLink>
            </li>
            <li>
            <NavLink to="/dashboard/reconstruct"> reconstruct </NavLink>
            </li>
            <li>
            <NavLink to="/dashboard/original"> original </NavLink>
            </li>
        </ul>
        </>
    )
}

export default Allsteps 

