import csv
import json
import os

# Define a function to convert CSV to JSON
def convert_csv_to_json(file):
    try:
        file_input_name = f"./csv/{file}.csv"
        file_output_name = f"./json/{file}.json"
        
        with open(file_input_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            json_data = list(reader)
            
            with open(file_output_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
        
        print(f"Converted {file}.csv to {file}.json")
    except Exception as error:
        print(f"Error converting {file}.csv:", error)

# Define a function to process files sequentially
def process_files():
    file = "address"
    convert_csv_to_json(file)

# Create the json directory if it doesn't exist
def create_json_directory():
    json_dir = os.path.join(os.getcwd(), "json")
    try:
        os.makedirs(json_dir, exist_ok=True)
        print("json directory created.")
    except Exception as error:
        print("Error creating json directory:", error)

# Call the function to create the json directory first
create_json_directory()

# Once the directory is created, start processing files
try:
    process_files()
    print("All files processed successfully.")
except Exception as error:
    print("Error processing files:", error)
