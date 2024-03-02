from flask import Flask, request, jsonify, send_file
import pandas as pd
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Enable CORS for React frontend

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER2 = 'standardise'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

modified_file = ''
standardised_data = ''  

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 402
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path) #contains input csv

        # Process the file: remove the first column
        data = pd.read_csv(file_path) 
        X = data.iloc[:, 1:] 
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        X.to_csv(processed_file_path, index=False)

        global modified_file
        modified_file = processed_file_path #contains output csv

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })

@app.route('/data', methods=['GET'])
def get_data():
    file_to_send = modified_file # taking input

    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 999
    
    X = pd.read_csv(file_to_send) 

    return send_file(file_to_send, as_attachment=True)

@app.route('/standardise', methods=['GET'])
def standardise_data():
    input_file = modified_file
    if not input_file:
        return jsonify({"error": "No data provided"}), 404

    data = pd.read_csv(input_file)
    print(f"IInput1 filename: {input_file}") # Debugging line

    # Standardize the data
    X_standardized, means, stds = standardize_data(data)

    global standardised_data

    filename = os.path.basename(modified_file)
    processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "2_" + filename)

    X_standardized.to_csv(processed_file_path, index=False)
    standardised_data = processed_file_path 

    return send_file(standardised_data, as_attachment=True)


def standardize_data(data):
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    X_standardized = (data - means) / stds
    return X_standardized, means, stds


if __name__ == "__main__":
    app.run(debug=True, port=5000)
