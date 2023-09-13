from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image
import os
import datetime

# Get the current date in the format YYYY-MM-DD
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

# Create the folder name with the current date
output_folder = f"barcode_images({current_date})"

def generate_barcode(text, output_filename):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Combine the output folder and filename to create the full output path
    full_output_path = os.path.join(output_folder, output_filename)
    
    code = Code39(text, writer=ImageWriter(), add_checksum=False)
    code.save(full_output_path)

def process_file(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if line:
                    barcode_filename = f"barcode_{line}.png"
                    generate_barcode(line, barcode_filename)

        print(f"Barcodes generated and saved to {output_folder}/")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    input_file = "split_output.txt"  # Replace with your input file name
    output_file = "output_data_barcode.txt"  # Replace with your desired output file name

    process_file(input_file, output_file)
