from flask import Flask, request, render_template_string, send_file, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Assuming the file is a CSV
            data = pd.read_csv(file)
            # Select only the first   10 columns
            selected_columns = data.iloc[:, :10]
            # Output CSV file path for selected columns
            output_csv_file = 'output10.csv'
            # Save the selected columns to a new CSV file
            selected_columns.to_csv(output_csv_file, index=False)
            # Render a template with a download button
            return render_template_string("""
            <p>File uploaded successfully. Click the button below to download the processed file.</p>
            <a href="{{ url_for('download_file') }}">Download Processed File</a>
            """, url_for=url_for)
    return render_template_string("""
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    """)

@app.route('/download')
def download_file():
    # Output CSV file path for selected columns
    output_csv_file = 'output10.csv'
    # Return the file for download
    return send_file(output_csv_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
