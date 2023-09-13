# Function to read data from a file, split it by ',' and write to a .txt document
def process_file(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            data = infile.read().strip()  # Read the file and remove leading/trailing whitespace
            items = data.split(',')  # Split data by ','

        with open(output_file, 'w') as outfile:
            for item in items:
                outfile.write(item.strip() + '\n')  # Write each item followed by a newline

        print(f"Data processed and saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    input_file = "input_file_to_split.txt"  # Replace with your input file name
    output_file = "split_output.txt"  # Replace with your desired output file name

    process_file(input_file, output_file)
