import json
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient("mongodb://phuong:705130665@147.129.181.20:11101/local")

# Define the database and collection
db = client['phuong_db']  # Replace with your database name
collection = db['faculties']  # Replace with your collection name

# Load JSON data
with open('faculty.json') as file:
    data = json.load(file)

# Insert data into MongoDB
if isinstance(data, list):
    # If the JSON data is an array of documents, use insert_many
    collection.insert_many(data)
else:
    # If the JSON data is a single document, use insert_one
    collection.insert_one(data)

print("Data inserted successfully.")
