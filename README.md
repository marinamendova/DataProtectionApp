# DataProtectionApp

## Overview
The Data Protection App is a Python-based application that applies differential privacy mechanisms to sensitive data. It offers two main methods for ensuring data privacy: the Laplace Mechanism and the Gaussian Mechanism. The app allows users to upload a CSV file, select a privacy method, specify parameters, and process the data to add noise for privacy protection. Processed data is saved in the same directory as the original file.

## Features
- Upload CSV files containing numeric data.
- Apply differential privacy mechanisms (Laplace and Gaussian).
- Configure privacy parameters (`epsilon` and `delta`).
- Save the processed (noisy) data to a new CSV file.
- Display information about `epsilon` and `delta` values.

## Requirements
- Python 3.x
- pandas
- numpy
- ttkbootstrap
- tkinter
- tkhtmlview
- diffprivlib
- matplotlib

## Installation
To run the application, ensure you have the required Python packages installed. You can install them using pip:

```bash
pip install pandas numpy ttkbootstrap tkhtmlview diffprivlib matplotlib
```

## Usage
1. **Run the Application**: Start the app by running the script.

    ```bash
    python data_protection_app.py
    ```

2. **Upload Data**: Click the "Upload Data" button to select a CSV file containing numeric data.

3. **Select Method**: Choose a differential privacy method from the dropdown menu.

4. **Configure Parameters**: 
   - Enter a value for `epsilon` (must be between 0 and 1).
   - If using the Gaussian Mechanism, enter a value for `delta` (must be between 0.001 and 1).

5. **Process Data**: Click the "Process Data" button to apply the chosen privacy mechanism and save the noisy data to a new file.

6. **View Information**: Click the `?` buttons next to `epsilon` and `delta` fields to learn more about selecting appropriate values for these parameters.

### Example
#### Uploading and Processing Data
1. Click "Upload Data" and select a file named `data.csv`.
2. Choose "Laplace Mechanism" from the dropdown.
3. Enter an `epsilon` value of `0.5`.
4. Click "Process Data".
5. The processed data will be saved as `data_protected.csv` in the same directory as the original file.

## Detailed Function Descriptions
### `validate_file(data)`
Checks if the file contains numeric data.

### `add_laplace_noise(data, epsilon)`
Adds Laplace noise to the data.

### `add_gaussian_noise(data, epsilon, delta)`
Adds Gaussian noise to the data.

### `apply_differential_privacy(data, method, epsilon, delta=None)`
Applies the selected differential privacy method to the data.

### `method_changed()`
Enables or disables the delta entry based on the selected method.

### `upload_data()`
Handles file upload and updates the interface accordingly.

### `save_data(data, original_path)`
Saves the processed data to a new CSV file.

### `preprocess_data(data)`
Preprocesses the data to ensure all values are numeric.

### `calculate_overall_mean(data)`
Calculates the overall mean of the data (for analytics purpose).

### `create_plot(original_mean, noisy_mean)`
Creates a bar plot comparing the original and noisy data means (for analytics purpose).

### `show_epsilon_info()`
Displays information about the `epsilon` parameter in a new window.

### `show_delta_info()`
Displays information about the `delta` parameter in a new window.

### `process_data()`
Main function to handle data processing, parameter validation, and error handling.

## GUI Components
- **Upload Data Button**: Initiates file upload dialog.
- **Data Label**: Displays the selected file name.
- **Method Menu**: Dropdown to select the privacy method.
- **Epsilon Entry**: Input field for `epsilon` value.
- **Delta Entry**: Input field for `delta` value.
- **Process Data Button**: Triggers the data processing.
- **Processed Data Label**: Indicates where the processed data is saved.
