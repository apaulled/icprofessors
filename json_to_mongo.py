import json
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient(host='147.129.181.20',
                     port=11101,
                     username='phuong',
                     password='705130665',
                     authSource='user-management',
                     authMechanism='SCRAM-SHA-256')

db = client['phuong_db']
collection = db['faculties']

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
