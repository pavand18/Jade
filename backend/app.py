from flask import Flask, request, jsonify, send_file
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

        global uploaded_filename
        uploaded_filename = processed_file_path #contains output csv

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        })


# @app.route('/data', methods=['GET'])
# def get_data():
#     file_to_send = uploaded_filename # Assuming 'uploaded_filename' is defined globally

#     if not file_to_send:
#         return jsonify({"error": "No filename provided"}), 999
    
#     # Construct the full path to the file
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_to_send)
    
#     if not os.path.exists(file_path):
#         return jsonify({"error": "File not found"}), 404
    
#     # Read the CSV file into a pandas DataFrame
#     df = pd.read_csv(file_path)
    
#     # Convert the DataFrame to JSON and return it
#     return jsonify(df.to_dict(orient='records'))


@app.route('/data', methods=['GET'])
def get_data():
    # file_to_send >> filename
    file_to_send = uploaded_filename # taking input

    if not file_to_send:
        return jsonify({"error": "No filename provided"}), 999
    
    X = pd.read_csv(file_to_send) 

    return send_file(file_to_send, as_attachment=True)






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
