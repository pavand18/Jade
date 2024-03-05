@app.route('/data', methods=['GET'])
def get_data():
    # taking input
    filename = uploaded_filename 
    if not filename:
        return jsonify({"error": "No filename provided"}), 999
    
    processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
    
    if not os.path.exists(processed_file_path):
        return jsonify({"error": "Processed file not found"}), 404
    
    X = pd.read_csv(processed_file_path)    
    print(f"SSSS: {X.head(1)}") # Debugging line

    print(f"IInput4 filename: {uploaded_filename}") # Debugging line
    print(f"IInput5 filename: {processed_file_path}") # Debugging line
    print(f"IInput6 filename: {uploaded_filename}") # Debugging line

    info = X.head(4).to_dict(orient='records', into=list)

    return jsonify({
        "shape": X.shape,
        "first_four_rows": X.head(4).to_dict(orient='records')
    })


import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import axios

const Data = () => {
 const [csvData, setCsvData] = useState(null);
 const [csvBlob, setCsvBlob] = useState(null);

 useEffect(() => {
    fetchCsvData();
 }, []);

 const fetchCsvData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/data', {
        responseType: 'blob', // Set the response type to blob to handle binary data
      });

      const blob = new Blob([response.data], { type: 'text/csv' });
      setCsvBlob(blob);

      // Convert the Blob to text
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        // Parse the CSV text
        const parsedData = parseCsv(text);
        setCsvData(parsedData);
      };
      reader.readAsText(blob);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
 };

 const parseCsv = (text) => {
    const lines = text.split('\n');
    const headers = lines[0].split(',');
    const data = lines.slice(1, 5).map(line => { // Only take the first 4 rows
      const values = line.split(',');
      const row = {};
      headers.forEach((header, index) => {
        row[header] = values[index];
      });
      return row;
    });
    return data;
 };

 const downloadCsv = () => {
    if (csvBlob) {
      const url = window.URL.createObjectURL(csvBlob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'data.csv');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    }
 };

 return (
    <div>
      {csvData ? (
        <div>
          <h2>CSV Data:</h2>
          <table>
            <thead>
              <tr>
                {Object.keys(csvData[0]).map((header, index) => (
                 <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csvData.map((row, rowIndex) => (
                <tr key={rowIndex}>
                 {Object.values(row).map((value, colIndex) => (
                    <td key={colIndex}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={downloadCsv}>Download CSV</button>
        </div>
      ) : (
        <p>Loading CSV data...</p>
      )}
    </div>
 );
};

export default Data;
