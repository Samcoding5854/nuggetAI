import csv
import json
from collections import defaultdict

# Load data from a CSV file
csv_file_path = "menu_data.csv"

with open(csv_file_path, "r") as file:
    csv_data = file.read()

# Parsing the CSV data
def parse_csv(csv_data):
    reader = csv.DictReader(csv_data.splitlines())
    data = defaultdict(lambda: {"menu_items": [], "special_features": []})
    
    for row in reader:
        restaurant = row["Restaurant"]
        item = {
            "item_name": row["Item Name"],
            "category": row["Category"],
            "veg_nonveg": row["Veg/NonVeg"],
            "price": int(row["Price"]),
            "description": row["Description"].strip(),
            "tags": [row["Category"].lower(), row["Veg/NonVeg"].lower()]
        }
        data[restaurant]["menu_items"].append(item)
        
        # Add special features (if applicable)
        if "veg" in row["Veg/NonVeg"].lower():
            data[restaurant]["special_features"].append("vegetarian")
        if "gluten-free" in row["Description"].lower():
            data[restaurant]["special_features"].append("gluten-free")

    return data

# Convert to JSON-friendly format
def convert_to_json(data):
    restaurant_data = []
    
    for restaurant, details in data.items():
        restaurant_entry = {
            "restaurant": restaurant,
            "menu_items": details["menu_items"],
            "location": "Downtown",  # You can adjust this based on your data
            "special_features": details["special_features"]
        }
        restaurant_data.append(restaurant_entry)
    
    return restaurant_data

# Parse CSV and convert to desired JSON format
parsed_data = parse_csv(csv_data)
json_data = convert_to_json(parsed_data)

# Output the result in JSON format
json_output = json.dumps(json_data, indent=2)
print(json_output)
