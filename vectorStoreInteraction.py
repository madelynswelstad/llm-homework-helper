import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('QDRANT_API_KEY')
k = 3
vectorDim = 4
distanceMetric = 'Cosine'

currentId = 0

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
                "size": vectorDim,
                "distance": distanceMetric
            }
        }
    }

    response = requests.put(url+'/collections/'+collectionName, json=payload, headers=headers)

    # print result
    if response.status_code == 200:
        print("Creation of collection successful!\n", response.json())
    else:
        print("Failed to create collection:", response.status_code, '\n', response.text)

    
def addDataPoint(collectionName, vectorizedDocument, currentId):
    # if getCollectionInfo(collectionName)
    print('size of vector:', len(vectorizedDocument))
    payload = {
        "points": [
            {
                "id": currentId,
                "vector": vectorizedDocument
            }
        ]
    }

    response = requests.put(f"{url}/collections/{collectionName}/points", json=payload, headers=headers)

    # print result
    if response.status_code == 200:
        currentId += 1
        print(f"Added a point to {collectionName} collection successful!\n", response.json())
    else:
        print(f"Failed to add point to {collectionName} collection:", response.status_code, '\n', response.text)


def getPointById(collectionName, pointId):
    response = requests.get(f"{url}/collections/{collectionName}/points/{pointId}", headers=headers)

    # print result
    if response.status_code == 200:
        print("Point retrieval successful!\nPoint data:", response.json())
    else:
        print(f"Failed to retrieve point with ID {pointId}:", response.status_code, '\n', response.text)

def getCollectionPoints(collectionName):
    response = requests.get(f"{url}/collections/{collectionName}/points", headers=headers)

    # print result
    if response.status_code == 200:
        print("Point retrieval successful!\nPoint data:", response.json())
    else:
        print(f"Failed to get points:", response.status_code, '\n', response.text)


# checkConnectionToStore()
# createCollection('testCollection')
addDataPoint('testCollection', [0.1, 0.2, 0.3, 0.4], currentId)
getPointById('testCollection', 0)
# getCollectionPoints('testCollection')