from flask import Flask, request, render_template_string, redirect, url_for
from flask_cors import CORS # Import CORS
import pandas as pd
import numpy as np
import os 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Enable CORS for all routes and methods


# Function to standardize the data
def standardize_data(data):
    # Calculate mean and standard deviation for each column
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    # Standardize the data
    X_standardized = (data - means) / stds
    
    return X_standardized, means, stds

def do_pca():
    X_standardized = pd.read_csv('standardised_data.csv')
    # Compute the covariance matrix
    cov_matrix = np.cov(X_standardized, rowvar=False)
    cov_matrix.shape
    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    # Sort eigenvectors and eigenvalues in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Specify the number of principal components you want to keep
    n_components = 9  # Adjust as needed

    # Construct principal components
    principal_components = eigenvectors[:, :n_components]
    # Project the original data onto the principal components
    X_pca = np.dot(X_standardized, principal_components)
    # Create a DataFrame for the compressed data
    compressed_data = pd.DataFrame(data=X_pca, columns=[f'PC{i+1}' for i in range(n_components)])
    # Save the compressed data to a CSV file
    output_file_path = 'pca_output.csv'
    compressed_data.to_csv(output_file_path, index=False)
    print(f"Compressed data saved to {output_file_path}")

    return X_standardized, principal_components , X_pca, compressed_data 

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
            # Avoid first column for analysis
            X = data.iloc[:,   1:]
            # Save the processed data to a temporary file
            temp_file = 'temp_data.csv'
            X.to_csv(temp_file, index=False)
            # Redirect to the visualization page
            return redirect(url_for('analyse'))
    return render_template_string("""
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Submit CSV">
    </form>
    """)

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'show_shape':
            # Load the processed data from the temporary file
            data = pd.read_csv('temp_data.csv')
            # Display the shape of the data
            output = f"<h1>Data Shape: {data.shape}</h1>"
        elif action == 'show_data':
            # Load the processed data from the temporary file
            data = pd.read_csv('temp_data.csv')
            # Display the first four rows of the data
            output = f"<p>{data.head(4).to_html()}</p>"
        elif action == 'standardise_data':
            # Load the processed data from the temporary file
            data = pd.read_csv('temp_data.csv')
            # Standardize the data and get means and standard deviations
            X_standardized, means, stds = standardize_data(data)
            # Output CSV file path for standardized data
            output_csv_file = 'standardised_data.csv'
            # Write the standardized data to a new CSV file
            X_standardized.to_csv(output_csv_file, index=False)
            # Output CSV file path for means and standard deviations
            stats_output_csv_file = 'mean_std_dev.csv'
            # Create a DataFrame for means and standard deviations
            stats_df = pd.DataFrame({'Mean': means, 'Standard_Deviation': stds})
            # Write means and standard deviations to a new CSV file
            stats_df.to_csv(stats_output_csv_file)
            output = f"<p>{X_standardized.head(4).to_html()}</p>"
        elif action == 'perform_pca':
            X_standardized, principal_components , X_pca, compressed_data = do_pca()
            #output of pca
            output = f"<p>{compressed_data.head(4).to_html()}</p>"
        elif action == 'reconstructed_standardised':
            # getting data..
            X_standardized, principal_components , X_pca, compressed_data = do_pca()

            ## main code ....
            X = pd.read_csv('temp_data.csv')
            # Reconstruct all columns from the compressed data
            reconstructed_data = np.dot(X_pca, principal_components.T)
            # Create a DataFrame for the reconstructed data
            reconstructed_df = pd.DataFrame(reconstructed_data, columns=X.columns)
            # Save the reconstructed data to a CSV file
            output_reconstructed_file_path = 'reconstructed_data.csv'
            reconstructed_df.to_csv(output_reconstructed_file_path, index=False)
            print(f"Reconstructed data saved to {output_reconstructed_file_path}")
            output = f"<p>{reconstructed_df.head(4).to_html()}</p>"
        elif action == 'original_data':
            # Function to reverse standardization
            def reverse_standardization(reconstructed_data, means, stds):
                # Reverse the standardization
                original_data = (reconstructed_data * stds) + means
                return original_data

            # Input CSV file paths
            reconstructed_data_csv_file = 'reconstructed_data.csv'
            mean_std_dev_csv_file = 'mean_std_dev.csv'

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
            output_csv_file = 'original_data.csv'

            # Write the original data to a new CSV file
            original_data.to_csv(output_csv_file, index=False)
            print("Original data saved to", output_csv_file)

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

            output = f"<p>{original_data.head(4).to_html()}</p>"
        else:
            output = "Please select an action."
        return render_template_string("""
        <form method="POST">
            <input type="submit" name="action" value="show_shape">
            <input type="submit" name="action" value="show_data">
            <input type="submit" name="action" value="standardise_data">
            <input type="submit" name="action" value="perform_pca">
            <input type="submit" name="action" value="reconstructed_standardised">
            <input type="submit" name="action" value="original_data">
        </form>
        """ + output)
    return render_template_string("""
    <form method="POST">
        <input type="submit" name="action" value="show_shape">
        <input type="submit" name="action" value="show_data">
        <input type="submit" name="action" value="standardise_data">
        <input type="submit" name="action" value="perform_pca">
        <input type="submit" name="action" value="reconstructed_standardised">
        <input type="submit" name="action" value="original_data">
    </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)
