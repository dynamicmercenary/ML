import subprocess

def check_and_install_library(library_name):
    try:
        __import__(library_name)
        print(f"{library_name} is installed.")
    except ImportError:
        print(f"{library_name} is not installed. Installing...")
        try:
            subprocess.check_call(['pip', 'install', library_name])
            print(f"{library_name} has been successfully installed.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {library_name}. Please install it manually.")

libraries_to_check = ['pandas', 'time', 'tkinter', 'os', 'openpyxl']

for library in libraries_to_check:
    check_and_install_library(library)
print("All libraries are installed, OK to proceed.")

import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import openpyxl

def open_files():
    file_paths = filedialog.askopenfilenames(
        title="Vælg CSV filerne, husk at de skal være navngivet korrekt", filetypes=[("CSV files", "*.csv")], multiple=True
    )

    if file_paths:
        try:
            # Read the first file
            filename1 = os.path.basename(file_paths[0])
            filename2 = os.path.basename(file_paths[1])
            if filename1.startswith('inc') or filename1.startswith('Inc'):
                df1 = pd.read_csv(file_paths[0])
                df2 = pd.read_csv(file_paths[1])
            elif not (filename2.startswith('inc') or filename2.startswith('Inc')):
                return print("Husk at navngiv filerne med Incident_måned_år.csv og CI_måned_år.csv")
            else:
                df1 = pd.read_csv(file_paths[1])
                df2 = pd.read_csv(file_paths[0])

    
            root.destroy()
            print("Files loaded successfully.")

            samlet_df = import_and_convert_data(df1, df2)
            excel_samlet = edit_xlsx(samlet_df)
            return delete_row_with_alro_and_cves(excel_samlet)
        except Exception as e:
            print(f"Error loading the files: {str(e)}")

def write_initial_text():
    initial_text = "Åben de filer som vi skal bruge på samme tid, altså ved at bruge ctrl-knap til at vælge flere filer."
    text_widget.config(state=tk.NORMAL) 
    text_widget.insert(tk.END, initial_text)  
    text_widget.config(state=tk.DISABLED) 

def import_and_convert_data(incident_måned_år, ci_måned_år):
    samlet = incident_måned_år.merge(ci_måned_år, left_on='Incident ID', right_on='User Incident ID')
    samlet = samlet.sort_values(by=['User Incident ID'])


    return samlet


def edit_xlsx(df):
    samlet = df

    samlet = samlet.drop(columns=['Incident Type', 'Requisition No', 'Order No', 'Assigned Team', 'Assigned To', 'Status', 'SLA Resolve By Deadline', 'Incident ID'])


    return samlet

def delete_row_with_alro_and_cves(df):
    samlet = df

    samlet = samlet.drop(samlet[(samlet['Customer Display Name'] == 'Allan Rosendahl') & (samlet['DisplayApproverFullName'] == 'Carina Vestergaard')].index)

    return samlet.to_excel('samlet_måned_år.xlsx', index=False, engine='openpyxl')

if __name__ == "__main__":

    root = tk.Tk()
    root.title("File Selection")

    root.geometry("600x400")


    open_button = tk.Button(root, text="Open Files", command=open_files)
    open_button.pack()

    text_widget = tk.Text(root, height=10, width=50, state=tk.DISABLED)
    text_widget.pack()


    write_initial_text()


    root.mainloop()
    print("Done")
