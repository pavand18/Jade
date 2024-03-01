from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np

# Create the Flask web server
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template_string("""
    <h1>Geekscoders.com, Hello Flask Application</h1>
    <a href="/contact">Contact</a><br>
    <a href="/about">About</a><br>
    <a href="/upload">Upload CSV</a>
    """)

# Route for the contact page
@app.route('/contact')
def contact():
    return "<h1>Geekscoders.com, Contact Page</h1>"

# Route for the about page
@app.route('/about')
def about():
    return "<h1>Geekscoders.com, About Page</h1>"

# Route for the CSV upload form
@app.route('/upload', methods=['GET', 'POST'])
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
            # Avoid first column for analysis
            X = data.iloc[:,  1:]
            # Perform your analysis here
            # For demonstration, let's just return the shape and first few rows
            return f"<h1>Data Shape: {data.shape}</h1><p>{X.head(4).to_html()}</p>"
    return render_template_string("""
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    """)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
