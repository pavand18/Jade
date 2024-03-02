from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np
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
standardised_file = ''  
compress_file = ''
g_X_pca = ''
g_principal_components = ''
g_X = ''
reconstructed_file = ''

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
        global g_X 
        g_X = X 

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


    filename = os.path.basename(modified_file)
    standardise_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "standardise_" + filename)
    
    X_standardized.to_csv(standardise_file_path, index=False)
    global standardised_file
    standardised_file = standardise_file_path #global file

    filename = os.path.basename(modified_file)
    mean_std_file = os.path.join(app.config['UPLOAD_FOLDER'], "mean_" + filename)
    stats_df = pd.DataFrame({'Mean': means, 'Standard_Deviation': stds})
    stats_df.to_csv(mean_std_file)

    return send_file(standardised_file, as_attachment=True)


def standardize_data(data):
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    X_standardized = (data - means) / stds
    return X_standardized, means, stds

@app.route('/dopca', methods=['GET'])
def dopca():
    X_standardized = pd.read_csv(standardised_file)
    cov_matrix = np.cov(X_standardized, rowvar=False)
    cov_matrix.shape
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    n_components = 7  # Adjust as needed
    principal_components = eigenvectors[:, :n_components]

    X_pca = np.dot(X_standardized, principal_components)
    compressed_data = pd.DataFrame(data=X_pca, columns=[f'PC{i+1}' for i in range(n_components)])

    filename = os.path.basename(modified_file)
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "compressed_" + filename)
    compressed_data.to_csv(compressed_file_path, index=False)

    global compress_file
    compress_file = compressed_file_path #global file
    global g_X_pca 
    g_X_pca = X_pca
    global g_principal_components    
    g_principal_components = principal_components #global file


    return send_file(compress_file, as_attachment=True)

@app.route('/reconstruct', methods=['GET'])
def reconstruct():
    X_pca = g_X_pca
    principal_components = g_principal_components
    X = g_X

    reconstructed_data = np.dot(X_pca, principal_components.T)
    reconstructed_df = pd.DataFrame(reconstructed_data, columns=X.columns)

    filename = os.path.basename(modified_file)
    reconstructed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "reconstructed_" + filename)
    reconstructed_df.to_csv(reconstructed_file_path, index=False)

    global reconstructed_file
    reconstructed_file = reconstructed_file_path #global file
    return send_file(reconstructed_file, as_attachment=True)

@app.route('/reconstruct', methods=['GET'])
def reconstruct():
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)

