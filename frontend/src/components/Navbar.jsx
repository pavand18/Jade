import { NavLink } from "react-router-dom";

function Navbar (){
  return(
    <>
      <ul>
        <li>
          <NavLink to="/"> Home </NavLink>
        </li>
        <li>
          <NavLink to="/about"> About </NavLink>
        </li>
        <li>
          <NavLink to="/contact"> Contact Us </NavLink>
        </li>
        <li>
          <NavLink to="/todo"> Todo </NavLink>
        </li>
        <li>
          <NavLink to="/fact"> Data </NavLink>
        </li>
        <li>
          <NavLink to="/fact2"> Data2 </NavLink>
        </li>
        <li>
          <NavLink to="/fact3"> Data3 </NavLink>
        </li>
      </ul>
    </>
  )
}

export default Navbar
