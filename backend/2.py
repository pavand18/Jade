from flask import Flask, request, jsonify, send_file
import pandas as pd
from flask_cors import CORS
import os
# from werkzeug.utils import secure_filename

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
        print(f"IInput3 filename: {file}") # Debugging line

        data = pd.read_csv(file) 
        X = data.iloc[:, 1:]
        processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file)

        global uploaded_filename
        X.to_csv(processed_file_path, index=False)
        uploaded_filename = file.processed_file_path

        print(f"IInput3 filename: {uploaded_filename}") # Debugging line
        # print(f"FFFF: {data.head(1)}") # Debugging line
        # print(f"SSSS: {X.head(1)}") # Debugging line
        

        # Return the shape and the first 4 rows of the processed data
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
        }) 

if __name__ == "__main__":
    app.run(debug=True, port=5000)