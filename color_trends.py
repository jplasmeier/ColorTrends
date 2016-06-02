#Takes a database of artwork, runs each artwork through the Clarifai API
#Appends a field for the colors of the image from Clafifai

import requests, json
from pymongo import MongoClient

client = MongoClient()

db = client.mydb

#Get the docs with a thumbnail url
db_cursor = db.tate.find({'thumbnailUrl':{ '$ne': ""}})[30005:40000]
size = 40000 - 30005
ind = 0
#db_cursor = db.tate.find({ 'title': 'Untitled A'})
for document in db_cursor:
    #read url from doc
    url = document['thumbnailUrl']
    #set args for GET request
    payload = {'model': 'general-v1.3', 'url': url, 'access_token':'oYenHf5YWPRY6Nxv0PEof3dUxG7XIq'}

    #make the get request, capture response
    print (ind /float(size))
    ind += 1
    resp = requests.get('https://api.clarifai.com/v1/color/',params=payload)

    color_json = resp.json()

    #add colors field to existing db object
    if color_json.get('status_code') == 'OK':
        colors = color_json.get('results')[0].get('colors')

    if document.get('colors') is None: 
         db.tate.update({"_id": document.get('_id')},{'$set': { "colors": colors}})

