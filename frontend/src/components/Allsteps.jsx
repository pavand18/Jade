import React from 'react';
import { NavLink } from "react-router-dom";
import "./Allsteps.css"; // Import CSS file for styling

function Allsteps() {
    return (
        <div className="all-steps-container">
            <ul className="steps-list">
                <li>
                    <NavLink to="/dashboard/data" className="step-button" activeClassName="active">Input</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard/standardise" className="step-button" activeClassName="active">Standardise</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard/submit" className="step-button" activeClassName="active">PCA</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard/reconstruct" className="step-button" activeClassName="active">Reconstruct</NavLink>
                </li>
                <li>
                    <NavLink to="/dashboard/original" className="step-button" activeClassName="active">Output</NavLink>
                </li>
            </ul>
        </div>
    );
}

export default Allsteps;




// import React from 'react';
// import { NavLink } from "react-router-dom";
// import { Nav } from 'react-bootstrap';
// import { Button } from 'react-bootstrap';

// function Allsteps() {
//   return (
//     <Nav variant="pills" className="justify-content-center">
//       <Nav.Item>
//         <Nav.Link as={NavLink} to="/dashboard/data" activeClassName="active">
//           <Button variant="outline-primary">Data</Button>
//         </Nav.Link>
//       </Nav.Item>
//       <Nav.Item>
//         <Nav.Link as={NavLink} to="/dashboard/standardise" activeClassName="active">
//           <Button variant="outline-primary">Standardise</Button>
//         </Nav.Link>
//       </Nav.Item>
//       <Nav.Item>
//         <Nav.Link as={NavLink} to="/dashboard/pca" activeClassName="active">
//           <Button variant="outline-primary">PCA</Button>
//         </Nav.Link>
//       </Nav.Item>
//       <Nav.Item>
//         <Nav.Link as={NavLink} to="/dashboard/reconstruct" activeClassName="active">
//           <Button variant="outline-primary">Reconstruct</Button>
//         </Nav.Link>
//       </Nav.Item>
//       <Nav.Item>
//         <Nav.Link as={NavLink} to="/dashboard/original" activeClassName="active">
//           <Button variant="outline-primary">Original</Button>
//         </Nav.Link>
//       </Nav.Item>
//     </Nav>
//   );
// }

// export default Allsteps;


// import React from 'react';
// import { NavLink } from "react-router-dom";
// import { Nav, Card } from 'react-bootstrap';
// import { Button } from 'react-bootstrap';
// // import './Allsteps.css'; // Import the CSS file

// function Allsteps() {
//     return (
//         <div className="allsteps-container">
//             <Card className="allsteps-card">
//                 <Card.Body>
//                     <Nav variant="pills" className="justify-content-center">
//                         <Nav.Item>
//                             <Nav.Link as={NavLink} to="/dashboard/data" activeClassName="active">
//                                 <Button variant="outline-primary">Data</Button>
//                             </Nav.Link>
//                         </Nav.Item>
//                         <Nav.Item>
//                             <Nav.Link as={NavLink} to="/dashboard/standardise" activeClassName="active">
//                                 <Button variant="outline-primary">Standardise</Button>
//                             </Nav.Link>
//                         </Nav.Item>
//                         <Nav.Item>
//                             <Nav.Link as={NavLink} to="/dashboard/pca" activeClassName="active">
//                                 <Button variant="outline-primary">PCA</Button>
//                             </Nav.Link>
//                         </Nav.Item>
//                         <Nav.Item>
//                             <Nav.Link as={NavLink} to="/dashboard/reconstruct" activeClassName="active">
//                                 <Button variant="outline-primary">Reconstruct</Button>
//                             </Nav.Link>
//                         </Nav.Item>
//                         <Nav.Item>
//                             <Nav.Link as={NavLink} to="/dashboard/original" activeClassName="active">
//                                 <Button variant="outline-primary">Original</Button>
//                             </Nav.Link>
//                         </Nav.Item>
//                     </Nav>
//                 </Card.Body>
//             </Card>
//             {/* Add another list here if needed */}
//         </div>
//     );
// }

// export default Allsteps;
