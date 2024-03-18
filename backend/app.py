from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
import numpy as np
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import flask
from collections import OrderedDict
import json
from collections import OrderedDict
import csv


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Enable CORS for React frontend
app.config["JSON_SORT_KEYS"] = False

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
g_mean_std_file = ''
g_original_file = ''
g_eigenvalues = ''
g_input_file = 'input.csv'
fake_output_file = 'output.csv'


def add_row_to_csv(input_file, output_file):
    # Read the existing CSV file
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Determine the number of columns in the CSV
    num_columns = len(data[0])

    # Create a new row with column numbers
    new_row = [str(i+1) for i in range(num_columns)]

    # Add the new row at the top of the data
    data.insert(0, new_row)

    # Write the modified data to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


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

        # add_row_to_csv(modified_file, fake_output_file)

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })


@app.route('/data', methods=['GET'])
def get_data():
    file_to_send = modified_file # Assuming the filename is passed as a query parameter
    add_row_to_csv(modified_file, fake_output_file)

    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 999
    
    X = pd.read_csv(fake_output_file)
    filename = os.path.basename(file_to_send)

    # Get the first 4 rows of the DataFrame
    first_four_rows = X.head(4).to_dict(orient='records')

    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })


# @app.route('/data', methods=['GET'])
# def get_data():
#     file_to_send = modified_file # taking input

#     if not file_to_send:
#         return jsonify({"error": "No filename provided"}), 999
    
#     X = pd.read_csv(file_to_send) 
#     filename = os.path.basename(modified_file)

#     # return send_file(file_to_send, as_attachment=True)
#     return send_from_directory('uploads', filename, as_attachment=True)

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

    filename = os.path.basename(modified_file)
    mean_std_file = os.path.join(app.config['UPLOAD_FOLDER'], "mean_" + filename)
    stats_df = pd.DataFrame({'Mean': means, 'Standard_Deviation': stds})
    stats_df.to_csv(mean_std_file)

    global standardised_file
    standardised_file = standardise_file_path #global file
    global g_mean_std_file
    g_mean_std_file = mean_std_file


    add_row_to_csv(standardise_file_path, fake_output_file)
    X_standardized_data = pd.read_csv(fake_output_file)

    first_four_rows = X_standardized_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

# @app.route('/standardise', methods=['GET'])
# def standardise_data():
#     input_file = modified_file      
#     if not input_file:
#         return jsonify({"error": "No data provided"}), 404

#     data = pd.read_csv(input_file)
#     print(f"IInput1 filename: {input_file}") # Debugging line

#     # Standardize the data
#     X_standardized, means, stds = standardize_data(data)


#     filename = os.path.basename(modified_file)
#     standardise_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "standardise_" + filename)
#     X_standardized.to_csv(standardise_file_path, index=False)

#     filename = os.path.basename(modified_file)
#     mean_std_file = os.path.join(app.config['UPLOAD_FOLDER'], "mean_" + filename)
#     stats_df = pd.DataFrame({'Mean': means, 'Standard_Deviation': stds})
#     stats_df.to_csv(mean_std_file)

#     global standardised_file
#     standardised_file = standardise_file_path #global file
#     global g_mean_std_file
#     g_mean_std_file = mean_std_file

#     f_filename = os.path.basename(standardise_file_path)
#     # return send_file(standardised_file, as_attachment=True)
#     return send_from_directory('uploads', f_filename, as_attachment=True)


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

    global g_eigenvalues
    g_eigenvalues = eigenvalues

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

    # return send_file(compress_file, as_attachment=True)

    add_row_to_csv(compress_file, fake_output_file)
    X_pca_data = pd.read_csv(fake_output_file)

    first_four_rows = X_pca_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })


# @app.route('/dopca', methods=['GET'])
# def dopca():
#     X_standardized = pd.read_csv(standardised_file)
#     cov_matrix = np.cov(X_standardized, rowvar=False)
#     cov_matrix.shape
#     eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
#     sorted_indices = np.argsort(eigenvalues)[::-1]
#     eigenvalues = eigenvalues[sorted_indices]
#     eigenvectors = eigenvectors[:, sorted_indices]

#     global g_eigenvalues
#     g_eigenvalues = eigenvalues

#     n_components = 7  # Adjust as needed
#     principal_components = eigenvectors[:, :n_components]

#     X_pca = np.dot(X_standardized, principal_components)
#     compressed_data = pd.DataFrame(data=X_pca, columns=[f'PC{i+1}' for i in range(n_components)])

#     filename = os.path.basename(modified_file)
#     compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "compressed_" + filename)
#     compressed_data.to_csv(compressed_file_path, index=False)

#     global compress_file
#     compress_file = compressed_file_path #global file
#     global g_X_pca 
#     g_X_pca = X_pca
#     global g_principal_components    
#     g_principal_components = principal_components #global file

#     return send_file(compress_file, as_attachment=True)


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
    # return send_file(reconstructed_file, as_attachment=True)

    add_row_to_csv(reconstructed_file, fake_output_file)
    X_reconstructed_data = pd.read_csv(fake_output_file)

    first_four_rows = X_reconstructed_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    }) 


@app.route('/original', methods=['GET'])
def original():
    # Input CSV file paths
    reconstructed_data_csv_file = reconstructed_file
    mean_std_dev_csv_file = g_mean_std_file

    # Read the standardized data from the CSV file
    reconstructed_data = pd.read_csv(reconstructed_data_csv_file)

    # Read means and standard deviations from the CSV file
    mean_std_dev_data = pd.read_csv(mean_std_dev_csv_file)

    # Extract means and standard deviations
    means = mean_std_dev_data['Mean'].values
    stds = mean_std_dev_data['Standard_Deviation'].values

    # Reverse the standardization to obtain the original data
    original_data = reverse_standardization(reconstructed_data, means, stds)

    # Output CSV file path for original data
    # output_csv_file = 'original_data.csv'

    filename = os.path.basename(modified_file)
    original_csv_file = os.path.join(app.config['UPLOAD_FOLDER'], "original_" + filename)
    original_data.to_csv(original_csv_file, index=False)
    global g_original_file 
    g_original_file = original_csv_file

    # Original data
    original_data_str = """Bus ODESSA 2 0 V pu,Bus ODESSA 2 0 V angle,Bus ODESSA 2 0 Frequency,Bus PRESIDIO 2 0 V pu,Bus PRESIDIO 2 0 V angle,Bus PRESIDIO 2 0 Frequency,Bus O DONNELL 1 0 V pu,Bus O DONNELL 1 0 V angle,Bus O DONNELL 1 0 Frequency,Bus O DONNELL 1 1 V pu,Bus O DONNELL 1 1 V angle,Bus O DONNELL 1 1 Frequency,Bus BIG SPRING 5 0 V pu,Bus BIG SPRING 5 0 V angle,Bus BIG SPRING 5 0 Frequency,Bus BIG SPRING 5 1 V pu,Bus BIG SPRING 5 1 V angle,Bus BIG SPRING 5 1 Frequency,Bus VAN HORN 0 V pu,Bus VAN HORN 0 V angle,Bus VAN HORN 0 Frequency,Bus IRAAN 2 0 V pu,Bus IRAAN 2 0 V angle,Bus IRAAN 2 0 Frequency,Bus IRAAN 2 1 V pu,Bus IRAAN 2 1 V angle,Bus IRAAN 2 1 Frequency,Bus PRESIDIO 1 0 V pu,Bus PRESIDIO 1 0 V angle,Bus PRESIDIO 1 0 Frequency,Bus PRESIDIO 1 1 V pu,Bus PRESIDIO 1 1 V angle,Bus PRESIDIO 1 1 Frequency,Bus SANDERSON 0 V pu,Bus SANDERSON 0 V angle,Bus SANDERSON 0 Frequency,Bus MONAHANS 2 0 V pu,Bus MONAHANS 2 0 V angle,Bus MONAHANS 2 0 Frequency,Bus GRANDFALLS 0 V pu,Bus GRANDFALLS 0 V angle,Bus GRANDFALLS 0 Frequency,Bus MARFA 0 V pu,Bus MARFA 0 V angle,Bus MARFA 0 Frequency,Bus GARDEN CITY 0 V pu,Bus GARDEN CITY 0 V angle,Bus GARDEN CITY 0 Frequency,Bus ODESSA 4 0 V pu,Bus ODESSA 4 0 V angle,Bus ODESSA 4 0 Frequency,Bus NOTREES 0 V pu,Bus NOTREES 0 V angle,Bus NOTREES 0 Frequency,Bus MIDLAND 4 0 V pu,Bus MIDLAND 4 0 V angle,Bus MIDLAND 4 0 Frequency,Bus BIG SPRING 1 0 V pu,Bus BIG SPRING 1 0 V angle,Bus BIG SPRING 1 0 Frequency,Bus BIG SPRING 1 1 V pu,Bus BIG SPRING 1 1 V angle,Bus BIG SPRING 1 1 Frequency,Bus O DONNELL 2 0 V pu,Bus O DONNELL 2 0 V angle,Bus O DONNELL 2 0 Frequency,Bus O DONNELL 2 1 V pu,Bus O DONNELL 2 1 V angle,Bus O DONNELL 2 1 Frequency,Bus ODESSA 6 0 V pu,Bus ODESSA 6 0 V angle,Bus ODESSA 6 0 Frequency,Bus BIG SPRINGS 0 V pu,Bus BIG SPRINGS 0 V angle,Bus BIG SPRINGS 0 Frequency,Bus BIG SPRINGS 1 V pu,Bus BIG SPRINGS 1 V angle,Bus BIG SPRINGS 1 Frequency,Bus MIDLAND 2 0 V pu,Bus MIDLAND 2 0 V angle,Bus MIDLAND 2 0 Frequency,Bus COAHOMA 0 V pu,Bus COAHOMA 0 V angle,Bus COAHOMA 0 Frequency,Bus MIDLAND 3 0 V pu,Bus MIDLAND 3 0 V angle,Bus MIDLAND 3 0 Frequency,Bus ALPINE 0 V pu,Bus ALPINE 0 V angle,Bus ALPINE 0 Frequency,Bus FORT DAVIS 0 V pu,Bus FORT DAVIS 0 V angle,Bus FORT DAVIS 0 Frequency,Bus MCCAMEY 1 0 V pu,Bus MCCAMEY 1 0 V angle,Bus MCCAMEY 1 0 Frequency,Bus KERMIT 0 V pu,Bus KERMIT 0 V angle,Bus KERMIT 0 Frequency,Bus ODESSA 1 0 V pu,Bus ODESSA 1 0 V angle,Bus ODESSA 1 0 Frequency,Bus ALPINE 1 0 V pu,Bus ALPINE 1 0 V angle,Bus ALPINE 1 0 Frequency,Bus ALPINE 1 1 V pu,Bus ALPINE 1 1 V angle,Bus ALPINE 1 1 Frequency,Bus MARFA 1 0 V pu,Bus MARFA 1 0 V angle,Bus MARFA 1 0 Frequency,Bus MARFA 1 1 V pu,Bus MARFA 1 1 V angle,Bus MARFA 1 1 Frequency,Bus MIDLAND 1 0 V pu,Bus MIDLAND 1 0 V angle,Bus MIDLAND 1 0 Frequency,Bus SEMINOLE 0 V pu,Bus SEMINOLE 0 V angle,Bus SEMINOLE 0 Frequency,Bus BIG SPRING 3 0 V pu,Bus BIG SPRING 3 0 V angle,Bus BIG SPRING 3 0 Frequency,Bus ODESSA 5 0 V pu,Bus ODESSA 5 0 V angle,Bus ODESSA 5 0 Frequency,Bus BIG SPRING 4 0 V pu,Bus BIG SPRING 4 0 V angle,Bus BIG SPRING 4 0 Frequency,Bus ODESSA 3 0 V pu,Bus ODESSA 3 0 V angle,Bus ODESSA 3 0 Frequency,Bus ODESSA 3 1 V pu,Bus ODESSA 3 1 V angle,Bus ODESSA 3 1 Frequency,Bus BIG SPRING 2 0 V pu,Bus BIG SPRING 2 0 V angle,Bus BIG SPRING 2 0 Frequency,Bus ALPINE 2 0 V pu,Bus ALPINE 2 0 V angle,Bus ALPINE 2 0 Frequency,Bus MARFA 2 0 V pu,Bus MARFA 2 0 V angle,Bus MARFA 2 0 Frequency,Bus MIDLAND 0 V pu,Bus MIDLAND 0 V angle,Bus MIDLAND 0 Frequency,Bus MONAHANS 1 0 V pu,Bus MONAHANS 1 0 V angle,Bus MONAHANS 1 0 Frequency,Bus MCCAMEY 2 0 V pu,Bus MCCAMEY 2 0 V angle,Bus MCCAMEY 2 0 Frequency,Bus SEMINOLE 1 0 V pu,Bus SEMINOLE 1 0 V angle,Bus SEMINOLE 1 0 Frequency,Bus MCCAMEY 0 V pu,Bus MCCAMEY 0 V angle,Bus MCCAMEY 0 Frequency,Bus MONAHANS 0 V pu,Bus MONAHANS 0 V angle,Bus MONAHANS 0 Frequency,Bus ODESSA 0 V pu,Bus ODESSA 0 V angle,Bus ODESSA 0 Frequency"""

    # Parsing the original data
    parsed_data = original_data_str.split(',')

    # Storing data in a dictionary
    bus_data = {}
    for item in parsed_data:
        parts = item.split()
        bus_name = ' '.join(parts[1:-3])  # Extracting bus name
        parameter = parts[-3]  # Extracting parameter (e.g., V pu, V angle, Frequency)
        value = parts[-1]  # Extracting value
        if bus_name not in bus_data:
            bus_data[bus_name] = {}
        bus_data[bus_name][parameter] = value

    # Printing the formatted output
    print("Bus Data:")
    for bus, parameters in bus_data.items():
        print(bus)
        for parameter, value in parameters.items():
            print(f"- {parameter}: {value}")

    # return send_file(original_csv_file, as_attachment=True)

    add_row_to_csv(original_csv_file, fake_output_file)
    X_original_data = pd.read_csv(fake_output_file)

    first_four_rows = X_original_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

# @app.route('/original', methods=['GET'])
# def original():
#     # Input CSV file paths
#     reconstructed_data_csv_file = reconstructed_file
#     mean_std_dev_csv_file = g_mean_std_file

#     # Read the standardized data from the CSV file
#     reconstructed_data = pd.read_csv(reconstructed_data_csv_file)

#     # Read means and standard deviations from the CSV file
#     mean_std_dev_data = pd.read_csv(mean_std_dev_csv_file)

#     # Extract means and standard deviations
#     means = mean_std_dev_data['Mean'].values
#     stds = mean_std_dev_data['Standard_Deviation'].values

#     # Reverse the standardization to obtain the original data
#     original_data = reverse_standardization(reconstructed_data, means, stds)

#     # Output CSV file path for original data
#     # output_csv_file = 'original_data.csv'

#     filename = os.path.basename(modified_file)
#     original_csv_file = os.path.join(app.config['UPLOAD_FOLDER'], "original_" + filename)
#     original_data.to_csv(original_csv_file, index=False)
#     global g_original_file 
#     g_original_file = original_csv_file

#     # Original data
#     original_data_str = """Bus ODESSA 2 0 V pu,Bus ODESSA 2 0 V angle,Bus ODESSA 2 0 Frequency,Bus PRESIDIO 2 0 V pu,Bus PRESIDIO 2 0 V angle,Bus PRESIDIO 2 0 Frequency,Bus O DONNELL 1 0 V pu,Bus O DONNELL 1 0 V angle,Bus O DONNELL 1 0 Frequency,Bus O DONNELL 1 1 V pu,Bus O DONNELL 1 1 V angle,Bus O DONNELL 1 1 Frequency,Bus BIG SPRING 5 0 V pu,Bus BIG SPRING 5 0 V angle,Bus BIG SPRING 5 0 Frequency,Bus BIG SPRING 5 1 V pu,Bus BIG SPRING 5 1 V angle,Bus BIG SPRING 5 1 Frequency,Bus VAN HORN 0 V pu,Bus VAN HORN 0 V angle,Bus VAN HORN 0 Frequency,Bus IRAAN 2 0 V pu,Bus IRAAN 2 0 V angle,Bus IRAAN 2 0 Frequency,Bus IRAAN 2 1 V pu,Bus IRAAN 2 1 V angle,Bus IRAAN 2 1 Frequency,Bus PRESIDIO 1 0 V pu,Bus PRESIDIO 1 0 V angle,Bus PRESIDIO 1 0 Frequency,Bus PRESIDIO 1 1 V pu,Bus PRESIDIO 1 1 V angle,Bus PRESIDIO 1 1 Frequency,Bus SANDERSON 0 V pu,Bus SANDERSON 0 V angle,Bus SANDERSON 0 Frequency,Bus MONAHANS 2 0 V pu,Bus MONAHANS 2 0 V angle,Bus MONAHANS 2 0 Frequency,Bus GRANDFALLS 0 V pu,Bus GRANDFALLS 0 V angle,Bus GRANDFALLS 0 Frequency,Bus MARFA 0 V pu,Bus MARFA 0 V angle,Bus MARFA 0 Frequency,Bus GARDEN CITY 0 V pu,Bus GARDEN CITY 0 V angle,Bus GARDEN CITY 0 Frequency,Bus ODESSA 4 0 V pu,Bus ODESSA 4 0 V angle,Bus ODESSA 4 0 Frequency,Bus NOTREES 0 V pu,Bus NOTREES 0 V angle,Bus NOTREES 0 Frequency,Bus MIDLAND 4 0 V pu,Bus MIDLAND 4 0 V angle,Bus MIDLAND 4 0 Frequency,Bus BIG SPRING 1 0 V pu,Bus BIG SPRING 1 0 V angle,Bus BIG SPRING 1 0 Frequency,Bus BIG SPRING 1 1 V pu,Bus BIG SPRING 1 1 V angle,Bus BIG SPRING 1 1 Frequency,Bus O DONNELL 2 0 V pu,Bus O DONNELL 2 0 V angle,Bus O DONNELL 2 0 Frequency,Bus O DONNELL 2 1 V pu,Bus O DONNELL 2 1 V angle,Bus O DONNELL 2 1 Frequency,Bus ODESSA 6 0 V pu,Bus ODESSA 6 0 V angle,Bus ODESSA 6 0 Frequency,Bus BIG SPRINGS 0 V pu,Bus BIG SPRINGS 0 V angle,Bus BIG SPRINGS 0 Frequency,Bus BIG SPRINGS 1 V pu,Bus BIG SPRINGS 1 V angle,Bus BIG SPRINGS 1 Frequency,Bus MIDLAND 2 0 V pu,Bus MIDLAND 2 0 V angle,Bus MIDLAND 2 0 Frequency,Bus COAHOMA 0 V pu,Bus COAHOMA 0 V angle,Bus COAHOMA 0 Frequency,Bus MIDLAND 3 0 V pu,Bus MIDLAND 3 0 V angle,Bus MIDLAND 3 0 Frequency,Bus ALPINE 0 V pu,Bus ALPINE 0 V angle,Bus ALPINE 0 Frequency,Bus FORT DAVIS 0 V pu,Bus FORT DAVIS 0 V angle,Bus FORT DAVIS 0 Frequency,Bus MCCAMEY 1 0 V pu,Bus MCCAMEY 1 0 V angle,Bus MCCAMEY 1 0 Frequency,Bus KERMIT 0 V pu,Bus KERMIT 0 V angle,Bus KERMIT 0 Frequency,Bus ODESSA 1 0 V pu,Bus ODESSA 1 0 V angle,Bus ODESSA 1 0 Frequency,Bus ALPINE 1 0 V pu,Bus ALPINE 1 0 V angle,Bus ALPINE 1 0 Frequency,Bus ALPINE 1 1 V pu,Bus ALPINE 1 1 V angle,Bus ALPINE 1 1 Frequency,Bus MARFA 1 0 V pu,Bus MARFA 1 0 V angle,Bus MARFA 1 0 Frequency,Bus MARFA 1 1 V pu,Bus MARFA 1 1 V angle,Bus MARFA 1 1 Frequency,Bus MIDLAND 1 0 V pu,Bus MIDLAND 1 0 V angle,Bus MIDLAND 1 0 Frequency,Bus SEMINOLE 0 V pu,Bus SEMINOLE 0 V angle,Bus SEMINOLE 0 Frequency,Bus BIG SPRING 3 0 V pu,Bus BIG SPRING 3 0 V angle,Bus BIG SPRING 3 0 Frequency,Bus ODESSA 5 0 V pu,Bus ODESSA 5 0 V angle,Bus ODESSA 5 0 Frequency,Bus BIG SPRING 4 0 V pu,Bus BIG SPRING 4 0 V angle,Bus BIG SPRING 4 0 Frequency,Bus ODESSA 3 0 V pu,Bus ODESSA 3 0 V angle,Bus ODESSA 3 0 Frequency,Bus ODESSA 3 1 V pu,Bus ODESSA 3 1 V angle,Bus ODESSA 3 1 Frequency,Bus BIG SPRING 2 0 V pu,Bus BIG SPRING 2 0 V angle,Bus BIG SPRING 2 0 Frequency,Bus ALPINE 2 0 V pu,Bus ALPINE 2 0 V angle,Bus ALPINE 2 0 Frequency,Bus MARFA 2 0 V pu,Bus MARFA 2 0 V angle,Bus MARFA 2 0 Frequency,Bus MIDLAND 0 V pu,Bus MIDLAND 0 V angle,Bus MIDLAND 0 Frequency,Bus MONAHANS 1 0 V pu,Bus MONAHANS 1 0 V angle,Bus MONAHANS 1 0 Frequency,Bus MCCAMEY 2 0 V pu,Bus MCCAMEY 2 0 V angle,Bus MCCAMEY 2 0 Frequency,Bus SEMINOLE 1 0 V pu,Bus SEMINOLE 1 0 V angle,Bus SEMINOLE 1 0 Frequency,Bus MCCAMEY 0 V pu,Bus MCCAMEY 0 V angle,Bus MCCAMEY 0 Frequency,Bus MONAHANS 0 V pu,Bus MONAHANS 0 V angle,Bus MONAHANS 0 Frequency,Bus ODESSA 0 V pu,Bus ODESSA 0 V angle,Bus ODESSA 0 Frequency"""

#     # Parsing the original data
#     parsed_data = original_data_str.split(',')

#     # Storing data in a dictionary
#     bus_data = {}
#     for item in parsed_data:
#         parts = item.split()
#         bus_name = ' '.join(parts[1:-3])  # Extracting bus name
#         parameter = parts[-3]  # Extracting parameter (e.g., V pu, V angle, Frequency)
#         value = parts[-1]  # Extracting value
#         if bus_name not in bus_data:
#             bus_data[bus_name] = {}
#         bus_data[bus_name][parameter] = value

#     # Printing the formatted output
#     print("Bus Data:")
#     for bus, parameters in bus_data.items():
#         print(bus)
#         for parameter, value in parameters.items():
#             print(f"- {parameter}: {value}")

#     return send_file(original_csv_file, as_attachment=True)


def reverse_standardization(reconstructed_data, means, stds):
        # Reverse the standardization
        original_data = (reconstructed_data * stds) + means
        return original_data

#adding plots..
@app.route('/plot1', methods=['GET'])
def plot1():
    original_data_toplot = modified_file
    original_column_data = pd.read_csv(original_data_toplot)

    # specify col. num. here
    data_from_particular_column = original_column_data.iloc[:, 4]
    start_index = 0  # Start index of the data points to select
    end_index = 200  # End index of the data points to select
    limited_data = data_from_particular_column[start_index:end_index]

    plt.figure(figsize=(6, 4))

    # Plot the limited data
    plt.plot(limited_data)
    plt.title('Plot of Input data')
    plt.xlabel('Index')
    plt.ylabel('Data')
    plt.grid(True) 

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()

    return {'plot_url': plot_url}

@app.route('/plot2', methods=['GET'])
def plot2():
    original_data_toplot = g_original_file
    original_column_data = pd.read_csv(original_data_toplot)

    # specify col. num. here
    data_from_particular_column = original_column_data.iloc[:, 4]
    start_index = 0  # Start index of the data points to select
    end_index = 200  # End index of the data points to select
    limited_data = data_from_particular_column[start_index:end_index]

    plt.figure(figsize=(6, 4))

    # Plot the limited data
    plt.plot(limited_data)
    plt.title('Plot of Reconstructed data')
    plt.xlabel('Index')
    plt.ylabel('Data')
    plt.grid(True) 

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()

    return {'plot_url': plot_url}

@app.route('/plot4', methods=['GET'])
def plot4():
    eigenvalues = g_eigenvalues
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, 10), eigenvalues[:9], marker='o')
    plt.title('Variance of First 9 Principal Components')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()

    return {'plot_url': plot_url}


@app.route('/plot3', methods=['GET'])
def plot3():
    file_path_1 = modified_file
    file_path_2 = g_original_file
    print(f"AAAA filename: {file_path_1}") # Debugging line
    print(f"BBBB filename: {file_path_2}") # Debugging line

    def load_and_select_data(file_path, column_index, start_index, end_index):
        reconstructed_column_data = pd.read_csv(file_path)
        data_from_column = reconstructed_column_data.iloc[:, column_index]
        return data_from_column[start_index:end_index]

    start_index = 0
    end_index = 200                         
    data_from_second_column_1 = load_and_select_data(file_path_1, 4, start_index, end_index)
    data_from_second_column_2 = load_and_select_data(file_path_2, 4, start_index, end_index)

    plt.figure(figsize=(8, 4))

    # Plot the limited data
    plt.plot(data_from_second_column_1, label='Input Plot')
    plt.plot(data_from_second_column_2, label='Reconstructed Plot')
    plt.title(f'Combined Plot (Indices: {start_index}-{end_index})')
    plt.xlabel('Index')
    plt.ylabel('Data')
    plt.grid(True)
    plt.legend()  # Add legend to distinguish between the two plots

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()
    plt.close()  # Close the figure after saving

    return {'plot_url': plot_url}

def load_and_select_data(file_path, column_index, start_index, end_index):
    reconstructed_column_data = pd.read_csv(file_path)
    data_from_column = reconstructed_column_data.iloc[:, column_index]
    return data_from_column[start_index:end_index]

@app.route('/plot5', methods=['GET'])
def plot5():
    file_path_1 = standardised_file
    file_path_2 = reconstructed_file
    print(f"AAAA filename: {file_path_1}") # Debugging line
    print(f"BBBB filename: {file_path_2}") # Debugging line

    def load_and_select_data(file_path, column_index, start_index, end_index):
        reconstructed_column_data = pd.read_csv(file_path)
        data_from_column = reconstructed_column_data.iloc[:, column_index]
        return data_from_column[start_index:end_index]

    start_index = 0
    end_index = 200                         
    data_from_second_column_1 = load_and_select_data(file_path_1, 4, start_index, end_index)
    data_from_second_column_2 = load_and_select_data(file_path_2, 4, start_index, end_index)

    plt.figure(figsize=(8, 4))

    # Plot the limited data
    plt.plot(data_from_second_column_1, label='Standardised Plot')
    plt.plot(data_from_second_column_2, label='Reconstructed_S Plot')
    plt.title(f'Combined Plot (Indices: {start_index}-{end_index})')
    plt.xlabel('Index')
    plt.ylabel('Data')
    plt.grid(True)
    plt.legend()  # Add legend to distinguish between the two plots

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()
    plt.close()  # Close the figure after saving

    return {'plot_url': plot_url}

def load_and_select_data(file_path, column_index, start_index, end_index):
    reconstructed_column_data = pd.read_csv(file_path)
    data_from_column = reconstructed_column_data.iloc[:, column_index]
    return data_from_column[start_index:end_index]

@app.route('/plot6', methods=['GET'])
def plot6():
    original_data_toplot = standardised_file
    original_column_data = pd.read_csv(original_data_toplot)

    # specify col. num. here
    data_from_particular_column = original_column_data.iloc[:, 4]
    start_index = 0  # Start index of the data points to select
    end_index = 200  # End index of the data points to select
    limited_data = data_from_particular_column[start_index:end_index]

    plt.figure(figsize=(6, 4))

    # Plot the limited data
    plt.plot(limited_data)
    plt.title('Plot of Standardised data')
    plt.xlabel('Index')
    plt.ylabel('Data')
    plt.grid(True) 

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_url = base64.b64encode(buf.read()).decode()

    return {'plot_url': plot_url}


if __name__ == "__main__":
    app.run(debug=True, port=5000)

