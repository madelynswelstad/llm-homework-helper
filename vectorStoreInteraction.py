import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('QDRANT_API_KEY')
k = 3
vectorDim = 4

url = 'https://071a9cd4-154f-4464-acfe-bb7a4ecb9770.us-east4-0.gcp.cloud.qdrant.io:6333'
headers = {"Authorization": "Bearer " + str(api_key),
           "Content-Type": "application/json"
}


def checkConnectionToStore():
    response = requests.get(url, headers=headers)

    # print result
    if response.status_code == 200:
        print("Connection successful!\n", response.json())
    else:
        print("Failed to connect:", response.status_code, '\n', response.text)

def createCollection(collectionName):
    payload = {
        "name": collectionName,
        "vectors": {
            "config": {
                "size": 4,
                "distance": "Cosine"
            }
        }
    }

    response = requests.put(url+'/collections/'+collectionName, json=payload, headers=headers)

    # print result
    if response.status_code == 200:
        print("Creation of collection successful!\n", response.json())
    else:
        print("Failed to create collection:", response.status_code, '\n', response.text)

# checkConnectionToStore()
createCollection('testCollection')