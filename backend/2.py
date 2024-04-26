import zipfile
from flask import Flask, request, jsonify, send_file, send_from_directory, make_response
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
from collections import OrderedDict
import csv
from flask import request
import os
from scipy.fft import dct, idct

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Enable CORS for React frontend
app.config["JSON_SORT_KEYS"] = False

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER2 = 'standardise'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


input_modified_file = ''
g_input_file_3 = ''
standardised_file = ''  
compress_file = ''
g_compress_file3 = ''
pc_data_file = ''
g_X_pca = ''
g_principal_components = []
g_X = ''
g_X_standardized = pd.DataFrame({})
reconstructed_file = ''
g_reconstructed_file_3 = ''
g_mean_std_file = ''
g_original_file = ''
g_eigenvalues = ''
g_input_file = 'input.csv'
fake_output_file = 'output.csv'
input_n2 = 0
input_n1 = 0
input_n3 = 0
input_n4 = 0
input_n5 = 0

# for sending data in order...
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



# >>> UPLOAD AND DATA
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
        X = data.iloc[:, 0:] 
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        X.to_csv(processed_file_path, index=False)

        global input_modified_file
        input_modified_file = processed_file_path #contains output csv
        global g_X 
        g_X = X 

        # add_row_to_csv(input_modified_file, fake_output_file)

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })

@app.route('/upload2', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files received'}), 400

        files = request.files.getlist('files')

        if not files:
            return jsonify({'success': False, 'error': 'No files received'}), 400

        for file in files:
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400

            if file and file.filename.endswith('.csv'):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                print(file_path)
                # You can perform further processing on the saved CSV file here
        
        data1 = ('uploads/compressed.csv')
        data2 = ('uploads/pc_data.csv')
        data3 = ('uploads/mean_std.csv')

        global compress_file
        compress_file = data1
        global pc_data_file
        pc_data_file = data2
        global g_mean_std_file
        g_mean_std_file = data3

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload3', methods=['POST'])
def upload_file3():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 401
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 402
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path) #contains input csv

        data = pd.read_csv(file_path) 

        global g_input_file_3
        g_input_file_3 = file_path

        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })

@app.route('/upload4', methods=['POST'])
def upload4():
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files received'}), 400

        files = request.files.getlist('files')

        if not files:
            return jsonify({'success': False, 'error': 'No files received'}), 400

        for file in files:
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400

            if file and file.filename.endswith('.csv'):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                print(file_path)
                # You can perform further processing on the saved CSV file here
        
        data2 = ('uploads/compress_dct.csv')
        data3 = ('uploads/mean_std_dct.csv')

        global g_compress_file3
        g_compress_file3 = data2 
        global g_mean_std_file
        g_mean_std_file = data3

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data3():
    file_to_send = input_modified_file # Assuming the filename is passed as a query parameter
    add_row_to_csv(input_modified_file, fake_output_file)

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

@app.route('/data2', methods=['GET'])
def send_file_info():
    try:
        file_info = []
        for file_path in [compress_file, pc_data_file, g_mean_std_file]:
            if file_path and os.path.isfile(file_path):
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                file_info.append({'name': file_name, 'size': file_size})

        if file_info:
            return jsonify({'success': True, 'files': file_info})
        else:
            return jsonify({'success': True, 'files': []})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/data3', methods=['GET'])
def get_data():
    file_to_send = g_input_file_3 # Assuming the filename is passed as a query parameter

    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 999
    
    X = pd.read_csv(file_to_send)

    # Get the first 4 rows of the DataFrame
    first_four_rows = X.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })



# >>> OPERATIONS <<<
@app.route('/standardise', methods=['GET'])
def standardise_data():
    input_file = input_modified_file      
    if not input_file:
        return jsonify({"error": "No data provided"}), 404

    data = pd.read_csv(input_file)
    print(f"IInput1 filename: {input_file}") # Debugging line

    # Standardize the data
    X_standardized, means, stds = standardize_data(data)


    filename = os.path.basename(input_modified_file)
    standardise_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "standardise.csv")
    X_standardized.to_csv(standardise_file_path, index=False, float_format='%.4f')

    filename = os.path.basename(input_modified_file)
    mean_std_file = os.path.join(app.config['UPLOAD_FOLDER'], "mean_std.csv")
    stats_df = pd.DataFrame({'Mean': means, 'Standard_Deviation': stds})
    stats_df.to_csv(mean_std_file)

    global standardised_file
    standardised_file = standardise_file_path #global file
    global g_mean_std_file
    g_mean_std_file = mean_std_file

    add_row_to_csv(standardise_file_path, fake_output_file)
    X_standardized_data = pd.read_csv(fake_output_file)

    first_four_rows = X_standardized_data.head(4).to_dict(orient='records')
    # first_four_rows = X_standardized_data(4).apply(lambda row: row[:20].to_dict(), axis=1).tolist()

    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

def standardize_data(data):
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    X_standardized = (data - means) / stds
    return X_standardized, means, stds

@app.route('/compress3', methods=['GET'])
def compression3():
    input_file = g_input_file_3
    pca_data = pd.read_csv(input_file)
    no_of_columns = pca_data.columns

    # Normalize data
    mean = np.mean(pca_data.values, axis=0)
    std = np.std(pca_data.values, axis=0)
    normalized_data = (pca_data.values - mean) / std

    # Initialize array to store compressed data
    compressed_data = np.zeros_like(pca_data.values)

    # Apply compression to each column separately
    for i in range(pca_data.shape[1]):
        # Apply DCT transformation to the current column
        transformed_column = dct(normalized_data[:, i], norm='ortho')
        
        # Define quantization threshold
        threshold = np.percentile(np.abs(transformed_column), 100 - 75) # Adjust as needed
        
        # Quantize the coefficients
        quantized_coeffs = transformed_column * (np.abs(transformed_column) >= threshold)
        
        # Save compressed data for the current column
        compressed_data[:, i] = quantized_coeffs

    # Save the compressed data to a CSV file
    compressed_pca_data = pd.DataFrame(compressed_data, columns=no_of_columns)
    filename = os.path.basename(input_file)
    compress_file3 = os.path.join(app.config['UPLOAD_FOLDER'], "compress_dct.csv")
    compressed_pca_data.to_csv(compress_file3, index=False, float_format='%.2f')

    # Create a DataFrame to store mean and std values
    mean_std_df = pd.DataFrame({'mean': mean, 'std': std})
    filename = os.path.basename(input_file)
    mean_std_file3 = os.path.join(app.config['UPLOAD_FOLDER'], "mean_std_dct.csv")
    mean_std_df.to_csv(mean_std_file3, index=False)
    
    global g_compress_file3
    g_compress_file3 = compress_file3
    global g_mean_std_file
    g_mean_std_file = mean_std_file3

    first_four_rows = compressed_pca_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

@app.route('/reconstruct3', methods=['GET'])
def reconstruct3():
    # Load compressed data from CSV file
    input_file = g_compress_file3
    compressed_pca_data = pd.read_csv(input_file)
    compressed_data = compressed_pca_data.values

    n_of_columns = compressed_pca_data.columns

    # Load mean and std values from "mean_std_file.csv"
    mean_std_file = g_mean_std_file
    mean_std_df = pd.read_csv(mean_std_file)
    mean = mean_std_df['mean'].values
    std = mean_std_df['std'].values

    # Initialize array to store reconstructed data
    reconstructed_data = np.zeros_like(compressed_data)

    # Apply decompression and reconstruction to each column separately
    for i in range(compressed_data.shape[1]):
        # Inverse DCT transformation
        reconstructed_column = idct(compressed_data[:, i], norm='ortho')
        
        # Denormalization
        reconstructed_column = (reconstructed_column * std[i]) + mean[i]
        
        # Store reconstructed data for the current column
        reconstructed_data[:, i] = reconstructed_column

    # Save the reconstructed data to a CSV file
    reconstructed_pca_data = pd.DataFrame(reconstructed_data, columns=n_of_columns)
    filename = os.path.basename(g_input_file_3)
    reconstructed_file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], "reconstructed_dct_file.csv")
    reconstructed_pca_data.to_csv(reconstructed_file_path3, index=False, float_format='%.4f')

    global g_reconstructed_file_3
    g_reconstructed_file_3 = reconstructed_file_path3
    
    first_four_rows = reconstructed_pca_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

@app.route('/dopca', methods=['GET'])
def dopca():
    n_components = request.args.get('n_components', default=2, type=int) # Adjust default as needed
    X_standardized = pd.read_csv(standardised_file)
    cov_matrix = np.cov(X_standardized, rowvar=False)
    cov_matrix.shape
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    global g_eigenvalues
    g_eigenvalues = eigenvalues

    print(f"XXXXXX number: {input_n3}")

    n_components = int(input_n3)  # Adjust as needed
    principal_components = eigenvectors[:, :n_components]
    pc_data = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])

    filename = os.path.basename(input_modified_file)
    pc_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "pc_data.csv")
    pc_data.to_csv(pc_file_path, index=False)

    X_pca = np.dot(X_standardized, principal_components)
    compressed_data = pd.DataFrame(data=X_pca, columns=[f'PC{i+1}' for i in range(n_components)])

    filename = os.path.basename(input_modified_file)
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "compressed.csv")
    compressed_data.to_csv(compressed_file_path, index=False, float_format='%.4f')

    global compress_file
    compress_file = compressed_file_path #global file
    global pc_data_file
    pc_data_file = pc_file_path
    global g_X_pca 
    g_X_pca = X_pca
    global g_principal_components    
    g_principal_components = principal_components #global file


    add_row_to_csv(compress_file, fake_output_file)
    X_pca_data = pd.read_csv(fake_output_file)

    first_four_rows = X_pca_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })

@app.route('/reconstruct', methods=['GET'])
def reconstruct():
    # X_pca = g_X_pca
    # principal_components = g_principal_components
    # mean_std_file = g_mean_std_file
    # mean_std_dev_data = pd.read_csv(mean_std_file)

    X_pca = pd.read_csv(compress_file)
    principal_components = pd.read_csv(pc_data_file)
    mean_std_file = g_mean_std_file
    mean_std_dev_data = pd.read_csv(mean_std_file)

    input_file_path = mean_std_file # Replace with your input file path
    df = pd.read_csv(input_file_path)

    first_column = df.iloc[:, 0]
    column_names_list = first_column.tolist()

    reconstructed_data = np.dot(X_pca, principal_components.T)
    reconstructed_df = pd.DataFrame(reconstructed_data, columns=column_names_list)

    filename = os.path.basename(input_modified_file)
    reconstructed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "reconstructed.csv")
    reconstructed_df.to_csv(reconstructed_file_path, index=False, float_format='%.4f')

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

    filename = os.path.basename(input_modified_file)
    original_csv_file = os.path.join(app.config['UPLOAD_FOLDER'], "reconstructed.csv")
    original_data.to_csv(original_csv_file, index=False, float_format='%.4f')
    
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

    add_row_to_csv(original_csv_file, fake_output_file)
    X_original_data = pd.read_csv(fake_output_file)

    # original_data
    first_four_rows = X_original_data.head(4).to_dict(orient='records')
    return jsonify({
        "success": True,
        "message": "File uploaded and processed successfully",
        "data": first_four_rows
    })



def reverse_standardization(reconstructed_data, means, stds):
        # Reverse the standardization
        original_data = (reconstructed_data * stds) + means
        return original_data



# >>> FILES AND RMSE <<<
@app.route('/get-file-sizes', methods=['GET'])
def get_file_sizes():
    global compress_file, pc_data_file, g_mean_std_file, input_modified_file

    input_file_size = os.path.getsize(input_modified_file)
    compressed_files_sizes = {
        'compress_file': os.path.getsize(compress_file),
        'pc_data_file': os.path.getsize(pc_data_file),
        'g_mean_std_file': os.path.getsize(g_mean_std_file),
    }

    return jsonify({
        'inputFileSize': input_file_size,
        'compressedFilesSizes': compressed_files_sizes,
    })

@app.route('/get-file-sizes3', methods=['GET'])
def get_file_sizes3():
    global g_compress_file3, g_mean_std_file

    compressed_files_sizes = {
        'compress_file': os.path.getsize(g_compress_file3),
        'g_mean_std_file': os.path.getsize(g_mean_std_file),
    }

    return jsonify({
        'compressedFilesSizes': compressed_files_sizes,
    })

@app.route('/calculate-rmse', methods=['GET'])
def calculate_rmse():
    input_file = input_modified_file
    output_file = g_original_file

    # Load original data
    original_data = pd.read_csv(input_file).values

    # Load reconstructed data
    reconstructed_data = pd.read_csv(output_file).values

    # Initialize variable to store total squared error
    total_squared_error = 0

    # Calculate squared error for each column
    for i in range(original_data.shape[1]):
        squared_error = np.sum((original_data[:, i] - reconstructed_data[:, i]) ** 2)
        total_squared_error += squared_error

    # Calculate RMSE (square root of average squared error)
    rmse = np.sqrt(total_squared_error / (original_data.shape[0] * original_data.shape[1]))

    return jsonify({'rmse': float(rmse)})  

@app.route('/calculate-rmse3', methods=['GET'])
def calculate_rmse3():
    input_file = g_input_file_3
    output_file = g_reconstructed_file_3

    # Load original data
    original_data = pd.read_csv(input_file).values

    # Load reconstructed data
    reconstructed_data = pd.read_csv(output_file).values

    # Initialize variable to store total squared error
    total_squared_error = 0

    # Calculate squared error for each column
    for i in range(original_data.shape[1]):
        squared_error = np.sum((original_data[:, i] - reconstructed_data[:, i]) ** 2)
        total_squared_error += squared_error

    # Calculate RMSE (square root of average squared error)
    rmse = np.sqrt(total_squared_error / (original_data.shape[0] * original_data.shape[1]))

    return jsonify({'rmse': float(rmse)})  

@app.route('/get-file-info', methods=['GET'])
def get_file_info():
    files = [compress_file, pc_data_file, g_mean_std_file]
    file_info = []
    for file_name in files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.exists(file_path):
            file_size_kb = os.path.getsize(file_path) / 1024
            file_info.append({'name': file_name, 'size': file_size_kb})
    return jsonify({'success': True, 'files': file_info})



# >>> DOWNLOAD FILES <<< 
@app.route('/download-files', methods=['GET'])  #1 zip
def download_files():
    global compress_file, pc_data_file, g_mean_std_file
    file_paths = [compress_file, pc_data_file, g_mean_std_file]

    # Create a zip file in memory
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zip_file:
        for file_path in file_paths:
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                zip_file.write(file_path, filename)

    zip_data.seek(0)

    # Create a response object with the zip file data
    response = make_response(zip_data.getvalue())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename=files.zip'

    return response

@app.route('/download-compressed-csv', methods=['GET']) #2 file
def download_compressed_csv():
    global g_original_file
    file_path = g_original_file

    # Check if the file exists
    if os.path.isfile(file_path):
        # Create a response object with the CSV file data
        response = make_response(send_file(file_path, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        response.headers['Content-Type'] = 'text/csv'

        return response
    else:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/download-files3', methods=['GET']) #3 zip
def download_files3():
    global g_compress_file3, g_mean_std_file
    file_paths = [g_compress_file3, g_mean_std_file]

    # Create a zip file in memory
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zip_file:
        for file_path in file_paths:
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                zip_file.write(file_path, filename)

    zip_data.seek(0)

    # Create a response object with the zip file data
    response = make_response(zip_data.getvalue())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename=files.zip'

    return response

@app.route('/download-4', methods=['GET'])  #4 file
def download_3():
    file_path = g_reconstructed_file_3

    # Check if the file exists
    if os.path.isfile(file_path):
        # Create a response object with the CSV file data
        response = make_response(send_file(file_path, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        response.headers['Content-Type'] = 'text/csv'

        return response
    else:
        return jsonify({"error": "File not found"}), 404



# >>> INPUT AND PLOT <<<
@app.route('/submit1', methods=['POST'])    #input
def submit1():
    data = request.get_json()
    number = data.get('number')
    if number:
        global input_n1 
        input_n1 = number    
        # Here you can process the number as needed
        print(f"Received number: {input_n1}")
        return jsonify({"message": "Number received successfully"}), 200
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route('/col1', methods=['GET'])    #input plot
def col1():
    file_to_send = input_modified_file
    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 400
    
    X = pd.read_csv(input_modified_file)
    colum = int(input_n1)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data,
        "data2": limited_data
    })

@app.route('/col3', methods=['GET'])    #input plot
def col3():
    file_to_send = g_input_file_3
    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 400
    
    X = pd.read_csv(file_to_send)
    colum = int(input_n1)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data,
        "data2": limited_data
    })

@app.route('/submit2', methods=['POST'])    #standardise
def submit2():
    data = request.get_json()
    number = data.get('number')
    if number:
        global input_n2 
        input_n2 = number    
        # Here you can process the number as needed
        print(f"Received number: {input_n2}")
        return jsonify({"message": "Number received successfully"}), 200
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route('/col2', methods=['GET'])    #stand plot
def col2():
    file_to_send = standardised_file
    if not file_to_send:                
        return jsonify({"error": "No filename provided"}), 400

    X = pd.read_csv(standardised_file)
    colum = int(input_n2)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data
    })

@app.route('/submit3', methods=['POST'])    #pca
def submit3():
    data = request.get_json()
    number = data.get('number')
    if number:
        global input_n3 
        input_n3 = number    
        # Here you can process the number as needed
        print(f"Received number: {input_n3}")
        return jsonify({"message": "Number received successfully"}), 200
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route('/submit4', methods=['POST'])    #reconstruct
def submit4():
    data = request.get_json()
    number = data.get('number')
    if number:
        global input_n4 
        input_n4 = number    
        # Here you can process the number as needed
        print(f"Received number: {input_n4}")
        return jsonify({"message": "Number received successfully"}), 200
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route('/rcol', methods=['GET'])    #reconstruct plot
def rcol():
    file_to_send = reconstructed_file
    if not file_to_send:                
        return jsonify({"error": "No filename provided"}), 400

    X = pd.read_csv(reconstructed_file)
    colum = int(input_n4)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data
    })

@app.route('/submit5', methods=['POST'])    #output
def submit5():
    data = request.get_json()
    number = data.get('number')
    if number:
        global input_n5 
        input_n5 = number    
        # Here you can process the number as needed
        print(f"Received number: {input_n5}")
        return jsonify({"message": "Number received successfully"}), 200
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route('/Ocol', methods=['GET'])    #output plot
def Ocol():
    file_to_send = g_original_file
    if not file_to_send:                
        return jsonify({"error": "No filename provided"}), 400

    X = pd.read_csv(g_original_file)
    colum = int(input_n5)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    X2 = pd.read_csv(input_modified_file)
    colum2 = int(input_n5)
    column_number2 = X2.iloc[:, colum2] # Adjust the index if the column is not the 4th one
    limited_data2 = column_number2[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data,
        "data2": limited_data2
    })

@app.route('/Ocol3', methods=['GET'])    #output plot
def Ocol3():
    X = pd.read_csv(g_reconstructed_file_3)
    colum = int(input_n5)
    column_number = X.iloc[:, colum] # Adjust the index if the column is not the 4th one
    limited_data = column_number[:1000].tolist()

    X2 = pd.read_csv(g_input_file_3)
    colum2 = int(input_n5)
    column_number2 = X2.iloc[:, colum2] # Adjust the index if the column is not the 4th one
    limited_data2 = column_number2[:1000].tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": limited_data,
        "data2": limited_data2
    })

@app.route('/var', methods=['GET'])     #var plot
def var():
    eigenvalues = g_eigenvalues
    eigenvalues_list = eigenvalues.tolist()

    return jsonify({
        "success": True,
        "message": "Data fetched successfully",
        "data": eigenvalues_list
    })



if __name__ == "__main__":
    app.run(debug=True, port=5000)





# most updated code....
