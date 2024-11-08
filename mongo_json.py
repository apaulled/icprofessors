import json

from bson import ObjectId
from pymongo import MongoClient
import mysql.connector

client = MongoClient(host='147.129.181.20',
                     port=11101,
                     username='lukas',
                     password='705148068',
                     authSource='user-management',
                     authMechanism='SCRAM-SHA-256')

db = client['lukas_db']
collection = db['ithacaFaculty']

faculty = [x for x in collection.find()]

with open('lukas_faculty.json', 'w') as file:
    for fac in faculty:
        fac['_id'] = str(fac['_id'])
    file.write(json.dumps(faculty, indent=4))
