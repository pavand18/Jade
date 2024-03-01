import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dashboard from '../components/Dashboard';

function Data() {
    const [dataShape, setDataShape] = useState(null);
    const [firstFourRows, setFirstFourRows] = useState([]);

    // Assuming the filename is stored in a state variable named 'filename'
    // You'll need to replace 'your_filename_here' with the actual filename
    const filename = 'your_filename_here';

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Include the filename as a query parameter in the request URL
                const response = await axios.get(`http://localhost:5000/data`);
                console.log(response.data);
                setDataShape(response.data.shape);
                setFirstFourRows(response.data.first_four_rows);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []); // Add filename as a dependency to re-fetch data when it changes

    return (
        <>
            <Dashboard />
            <h2>Data</h2>
            <p>Shape: {dataShape ? `${dataShape[0]} rows, ${dataShape[1]} columns` : 'Loading...'}</p>
            <h3>First 4 Rows:</h3>
            <table>
                <thead>
                    <tr>
                        {firstFourRows.length > 0 && Object.keys(firstFourRows[0]).map((key) => (
                            <th key={key}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {firstFourRows.map((row, index) => (
                        <tr key={index}>
                            {Object.values(row).map((value, i) => (
                                <td key={i}>{value}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
}

export default Data;
