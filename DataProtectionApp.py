import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox as msg, Toplevel
from tkinter import *
from tkhtmlview import HTMLLabel
from tkinter import Toplevel
from diffprivlib.mechanisms import Laplace, Gaussian
import matplotlib.pyplot as plt
import os

# Function to validate if the uploaded file contains numeric data
def validate_file(data):
    if not any(np.issubdtype(dtype, np.number) for dtype in data.dtypes):
        return False
    return True

# Function to add Laplace noise to the data
def add_laplace_noise(data, epsilon):
    if epsilon == 0:
        msg.showerror("Error", "Epsilon must be non-zero.")
        return None

    mech = Laplace(epsilon=epsilon, sensitivity=1)
    noisy_data = data.apply(mech.randomise)
    return noisy_data

# Function to add Gaussian noise to the data
def add_gaussian_noise(data, epsilon, delta):
    if epsilon == 0 or delta == 0:
        msg.showerror("Error", "Epsilon and delta must be non-zero.")
        return None

    sensitivity = np.sqrt(np.sum(np.square(data.values.flatten())))
    mech = Gaussian(epsilon=epsilon, delta=delta, sensitivity=sensitivity)
    noisy_data = data.apply(mech.randomise)
    return noisy_data

# Function to apply differential privacy to the data based on the selected method
def apply_differential_privacy(data, method, epsilon, delta=None):
    if epsilon == 0:
        msg.showerror("Error", "Epsilon must be non-zero.")
        return None

    if method == "Laplace Mechanism":
        if epsilon <= 0:
            msg.showerror("Error", "Epsilon must be greater than 0.")
            return None
        elif epsilon > 1:
            msg.showerror("Error", "Epsilon can't be greater than 1.")
            return None
        protected_data = add_laplace_noise(data, epsilon)
        return protected_data

    elif method == "Gaussian Mechanism":
        if delta is None:
            msg.showerror("Error", "Delta must be provided for Gaussian Mechanism.")
            return None

        if epsilon <= 0:
            msg.showerror("Error", "Epsilon must be greater than 0.")
            return None
        elif epsilon > 1:
            msg.showerror("Error", "Epsilon can't be greater than 1.")
            return None

        protected_data = add_gaussian_noise(data, epsilon, delta)
        return protected_data

    print(f"Method '{method}' not supported yet. Returning original data.")
    return data

# Function to handle method change and enable/disable delta entry accordingly
def method_changed(*args):
    if method_var.get() == "Laplace Mechanism":
        delta_entry.config(state="disabled")
    else:
        delta_entry.config(state="normal")

# Function to upload data file
def upload_data():
    global data_path
    global epsilon_entry
    global delta_entry

    data_path = filedialog.askopenfilename(
        title="Select Data File",
        filetypes=[("CSV files", "*.csv")]
    )

    if data_path:
        data_label.config(text=f"File Selected: {data_path.split('/')[-1]}")
        epsilon_entry.config(state="normal")
        method_changed()

# Function to save the protected data to a new file
def save_data(data, original_path):
    directory, filename = os.path.split(original_path)
    new_path = os.path.join(directory, filename.replace('.csv', '_protected.csv'))

    if os.path.exists(new_path):
        try:
            os.remove(new_path)
        except PermissionError:
            msg.showerror("Error", f"Cannot write to file {new_path}. Please close the file if it is open in another application.")
            return

    try:
        data.to_csv(new_path, index=False)
        msg.showinfo("Success", f"Protected data saved to {new_path}")
    except PermissionError:
        msg.showerror("Error", f"Permission denied: {new_path}. Unable to save the file.")

# Function to preprocess data by converting to numeric and filling NaNs
def preprocess_data(data):
    data = data.apply(pd.to_numeric, errors='coerce').fillna(0)
    return data

# Function to calculate the overall mean of the data (for analytics purpose)
def calculate_overall_mean(data):
    return data.values.flatten().mean()

# Function to create a plot comparing the means of original and noisy data (for analytics purpose)
def create_plot(original_mean, noisy_mean):
    plt.figure(figsize=(8, 6))
    categories = ['Средна стойност на оригинални данни', 'Средна стойност на зашумени данни']
    values = [original_mean, noisy_mean]

    plt.bar(categories, values, color=['blue', 'orange'])
    plt.ylabel('Средна стойност')
    plt.title('Сравнение на средни стойности')
    plt.ylim([min(values) * 0.9, max(values) * 1.1])

    for i, v in enumerate(values):
        plt.text(i, v + (max(values) - min(values)) * 0.02, f'{v:.2f}', ha='center', fontweight='bold')

    plt.show()

# Function to show information about epsilon
def show_epsilon_info():
    info_window = Toplevel(root)
    info_window.title("Epsilon Information")
    info_window.geometry("1000x800")

def show_epsilon_info():
    info_window = Toplevel()
    info_window.title("Epsilon Information")
    info_window.geometry("800x800")

    html_text = """
    <body style="font-family: Calibri, sans-serif; margin: 20px; padding: 0; background-color: white;">
    <h2 style="font-size: 14px; text-align: center">Препоръки за избор на стойност на епсилон (ε)</h2>
    <p style="font-size: 10px;">Параметърът <b>епсилон (ε)</b>, т.нар. параметър за поверителност или бюджет за поверителност, контролира нивото на защита на данните при прилагането на диференциална поверителност. Изборът на подходяща стойност на ε е от съществено значение за балансирането между поверителността и точността на резултатите.</p>
    <p style="font-size: 10px;">Стойността на епсилон трябва да е <b>по-голяма от 0 и по-малка от 1.</b> Определянето на най-подходящата стойност зависи изцяло от Вашите нужди и цели. Ето няколко препоръки, които могат да ви помогнат да изберете подходящата стойност на ε:
    <ul style="font-size: 10px;">
        <li>Ако данните са <b>изключително чувствителни</b> (напр. медицински записи, лична финансова информация и др.), изберете <b>по-ниска стойност</b> на ε (напр. 0.01 или 0.1). Това ще осигури висока степен на защита на поверителността, но ще добави повече шум към данните, което може да намали точността на анализите.</li>
        <li>Ако е необходимо да се запази <b>висока точност на анализите</b> и данните не са изключително чувствителни, можете да изберете <b>по-висока стойност</b> на ε (напр. 0.5 или 0.8). Това ще добави по-малко шум и ще запази полезността на данните, но защитата на поверителността ще бъде по-слаба.</li>
    </ul>
    <h3 style="font-size: 10px;">Примери за стойности на ε:</h3>
    <ul style="font-size: 10px;">
        <li><b>Много висока поверителност</b>: ε = 0.01</li>
        <li><b>Висока поверителност</b>: ε = 0.1</li>
        <li><b>Средна поверителност</b>: ε = 0.5</li>
        <li><b>Ниска поверителност</b>: ε = 0.8</li>
    </ul>
    <p style="font-size: 10px;">Имайте предвид, че изборът на стойност на ε трябва да бъде съобразен с анализа на риска, свързан с потенциалната загуба на конфиденциалност. По-ниски стойности на ε намаляват риска от разкриване на лична информация, но увеличават несигурността в анализа на данните.</p>
    </body>
    """

    html_label = HTMLLabel(info_window, html=html_text)
    html_label.pack(padx=10, pady=10, fill="both", expand=True)

# Function to show information about delta
def show_delta_info():
    info_window = Toplevel()
    info_window.title("Delta Information")
    info_window.geometry("800x800")

    html_text = """
    <body style="font-family: Calibri, sans-serif; margin: 20px; padding: 0; background-color: white;">
    <h2 style="font-size: 14px; text-align: center">Препоръки за избор на стойност на делта (δ)</h2>
    <p style="font-size: 10px;">Параметърът <b>δ</b> в Гаусовия механизъм контролира нивото на допълнителна защита на данните при прилагането на диференциална поверителност. Изборът на подходяща стойност на δ е от съществено значение за балансирането между поверителността и точността на резултатите.</p>
    <p style="font-size: 10px;">Стойността на δ трябва да бъде число между 0.001 и 1. Определянето на най-подходящата стойност зависи изцяло от Вашите нужди и цели. Ето няколко препоръки, които могат да ви помогнат да изберете подходящата стойност на δ:
    <ul style="font-size: 10px; text-align: left; margin: 5px;">
        <li>Ако данните са <b>изключително чувствителни</b> (напр. медицински записи, лична финансова информация и др.), изберете <b>по-ниска стойност</b> на δ (напр. 0.001). Това ще осигури висока степен на защита на поверителността, но може да намали точността на анализите.</li>
        <li>Ако е необходимо да се запази <b>висока точност на анализите</b> и данните не са изключително чувствителни, можете да изберете <b>по-висока стойност</b> на δ (напр. 0.1). Това ще запази полезността на данните, но защитата на поверителността ще бъде по-слаба.</li>
    </ul>
    <h3 style="font-size: 10px; margin: 5px;">Примери за стойности на δ:</h3>
    <ul style="font-size: 10px; text-align: left; margin: 5px;">
        <li><b>Много висока защита</b>: δ = 0.001</li>
        <li><b>Висока защита</b>: δ = 0.01</li>
        <li><b>Средна защита</b>: δ = 0.1</li>
        <li><b>Ниска защита</b>: δ = 0.5</li>
    </ul>
    <p style="font-size: 10px; text-align: left; margin: 5px;">Имайте предвид, че изборът на стойност на δ трябва да бъде съобразен с анализа на риска, свързан с потенциалната загуба на конфиденциалност. По-ниски стойности на δ намаляват риска от разкриване на лична информация, но увеличават несигурността в анализа на данните.</p>
    </body>
    """

    html_label = HTMLLabel(info_window, html=html_text)
    html_label.pack(padx=10, pady=10, fill="both", expand=True)

# Function to handle the main flow
def process_data():
    if not data_path:
        msg.showerror("Error", "Please upload a data file.")
        return

    if not method_var.get() or method_var.get() == "Select Method":
        msg.showerror("Error", "Please select a method.")
        return

    if data_path:
        if data_path.endswith(".csv"):
            try:
                data = pd.read_csv(data_path)
                data_label.config(text=f"File Selected: {data_path.split('/')[-1]}")
            except pd.errors.ParserError:
                msg.showerror("Error", "Invalid CSV format. Please ensure proper comma separation.")
                return
        else:
            msg.showerror("Error", "Please select a CSV file for processing.")
            return

        if not validate_file(data):
            msg.showerror("Error", "The file does not contain numeric values. Please upload a valid file with numeric data.")
            return

        epsilon_input = epsilon_entry.get()
        if not epsilon_input:
            msg.showerror("Error", "Please enter a value for epsilon.")
            return

        epsilon_input = epsilon_input.replace(",", ".")
        try:
            epsilon = float(epsilon_input)
        except ValueError:
            msg.showerror("Error", "Invalid value for epsilon. Please enter a valid number.")
            return

        if epsilon <= 0:
            msg.showerror("Error", "Epsilon must be greater than 0.")
            return None
        elif epsilon > 1:
            msg.showerror("Error", "Epsilon can't be greater than 1.")
            return None

        delta = None
        if method_var.get() == "Gaussian Mechanism":
            delta_input = delta_entry.get()
            if not delta_input:
                msg.showerror("Error", "Please enter a value for delta.")
                return

            delta_input = delta_input.replace(",", ".")
            try:
                delta = float(delta_input)
            except ValueError:
                msg.showerror("Error", "Invalid value for delta. Please enter a valid number.")
                return

            if delta < 0.001 or delta > 1:
                msg.showerror("Error", "Delta must be a number between 0.001 and 1.")
                return

        preprocessed_data = preprocess_data(data)

        protected_data = preprocessed_data
        for column in preprocessed_data.columns:
            try:
                column_data = preprocessed_data[column]
                protected_column = apply_differential_privacy(column_data, method_var.get(), epsilon, delta)
                if protected_column is not None:
                    protected_data[column] = protected_column
            except Exception as e:
                msg.showerror("Error", f"An unexpected error occurred while processing column '{column}': {str(e)}")
                return

        original_mean = calculate_overall_mean(preprocessed_data)
        noisy_mean = calculate_overall_mean(protected_data)
        #create_plot(original_mean, noisy_mean)

        save_data(protected_data, data_path)

# GUI setup
root = ttk.Window(themename="darkly")
root.title("Data Protection App")
root.geometry("800x600")

data_path = ""

upload_button = ttk.Button(root, text="Upload Data", command=upload_data, bootstyle="primary")
upload_button.pack(side="top", padx=10, pady=10, ipadx=20, ipady=20)

data_label = ttk.Label(root, text="No file selected")
data_label.pack(padx=10, pady=10)

method_var = ttk.StringVar(root)
method_var.set("Select Method")
method_menu = ttk.OptionMenu(root, method_var, "Select Method", "Laplace Mechanism", "Gaussian Mechanism")
method_menu.pack(padx=10, pady=30)
method_var.trace_add('write', method_changed)

epsilon_label = ttk.Label(root, text="Epsilon (0-1):")
epsilon_label.pack(padx=10, pady=3)
epsilon_frame = ttk.Frame(root)
epsilon_frame.pack(padx=10, pady=3)
epsilon_entry = ttk.Entry(epsilon_frame, state="disabled")
epsilon_entry.pack(side="left", padx=(5, 5))
epsilon_info_button = ttk.Button(epsilon_frame, text="?", command=show_epsilon_info, bootstyle="info")
epsilon_info_button.pack(side="left")

delta_label = ttk.Label(root, text="Delta (0.001-1):")
delta_label.pack(padx=10, pady=3)
delta_frame = ttk.Frame(root)
delta_frame.pack(padx=10, pady=3)
delta_entry = ttk.Entry(delta_frame, state="disabled")
delta_entry.pack(side="left", padx=(5, 5))
delta_info_button = ttk.Button(delta_frame, text="?", command=show_delta_info, bootstyle="info")
delta_info_button.pack(side="left")

process_button = ttk.Button(root, text="Process Data", command=process_data, bootstyle="success")
process_button.pack(side="top", padx=10, pady=10, ipadx=20, ipady=20)

processed_data_label = ttk.Label(root, text="Processed data will be saved in the same directory")
processed_data_label.pack(padx=10, pady=10)

root.mainloop()
