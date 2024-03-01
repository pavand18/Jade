from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Enable CORS for React frontend

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

uploaded_filename = ''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        

        # Process the file: remove the first column
        data = pd.read_csv(file_path) 
        X = data.iloc[:, 1:] 
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        X.to_csv(processed_file_path, index=False)

        global uploaded_filename
        uploaded_filename = filename
        print(f"IInput3 filename: {uploaded_filename}") # Debugging line
        print(f"FFFF: {X.head(1)}") # Debugging line

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })

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

@app.route('/standardise', methods=['POST'])
def standardise_data():
    data = request.json.get('data', [])
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Convert the list of lists to a DataFrame
    df = pd.DataFrame(data)

    # Standardize the data
    X_standardized, means, stds = standardize_data(df)

    # Convert the DataFrame back to a list of lists
    standardized_data = X_standardized.values.tolist()

    return jsonify({
        "standardizedData": standardized_data,
        "means": means.tolist(),
        "stds": stds.tolist(),
    })

def standardize_data(data):
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    X_standardized = (data - means) / stds
    return X_standardized, means, stds


if __name__ == "__main__":
    app.run(debug=True, port=5000)
