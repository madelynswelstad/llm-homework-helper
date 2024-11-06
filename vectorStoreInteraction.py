import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('QDRANT_API_KEY')
k = 3
vectorDim = 4
collectionName = ''

url = 'https://071a9cd4-154f-4464-acfe-bb7a4ecb9770.us-east4-0.gcp.cloud.qdrant.io:6333'
headers = {"Authorization": "Bearer " + str(api_key)}


def checkConnectionToStore():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Connection successful!\n", response.json())
    else:
        print("Failed to connect:", response.status_code, '\n', response.text)

def addData():
    payload = {
        "name": "collection_name",
        "vectors": {
            "size": vectorDim,
            "distance": "cosine"
        }
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Connection successful!\n", response.json())
    else:
        print("Failed to connect:", response.status_code, '\n', response.text)

# response = requests.post(url, json=payload, headers=headers) # send POST request

# def getKNearestNeighbors(vectorizedQuery):

checkConnectionToStore()