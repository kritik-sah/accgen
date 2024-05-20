import json

def extract_addresses(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:  # Specify encoding as 'utf-8'
        data = json.load(f)
        addresses = [item.get('address', '') for item in data]
        return addresses

def append_addresses_to_txt(addresses, txt_file_path):
    with open(txt_file_path, 'a', encoding='utf-8') as f:  # Open file in append mode
        for address in addresses:
            f.write(address.lower() + '\n')

if __name__ == "__main__":
    json_file_path = "address.json"  # Update with your JSON file path
    txt_file_path = "addresses.txt"  # Update with desired output file path

    addresses = extract_addresses(json_file_path)
    append_addresses_to_txt(addresses, txt_file_path)

    print("Addresses appended to addresses.txt successfully!")
