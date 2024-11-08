import json

# This file basically just exists so that I know exactly what potential columns exist in the Mongo DB

with open('lukas_faculty.json') as file:
    data = json.loads(file.read())
    keys = set()
    for fac in data:
        for key in fac.keys():
            keys.add(key)
    print(keys)
