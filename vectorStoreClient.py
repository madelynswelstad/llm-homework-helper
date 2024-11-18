import os
import openai
from dotenv import load_dotenv, find_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

client = QdrantClient(
    url="https://071a9cd4-154f-4464-acfe-bb7a4ecb9770.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=os.getenv('QDRANT_API_KEY')
)

collection_name_test = 'llm_training_data'
vector_size = 100
distance_metric = Distance.COSINE

def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance_metric),
    )

# same as embeddings.py, but does one at a time
def get_embedding(text):
    response = openai.Embedding.create(
        input=text, # input must be pdf
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def insert_documents(documents, collection_name):
    points = [
        PointStruct(
            id=doc['id'],
            vector=get_embedding(doc['text']),
            payload={"text": doc['text']}
        )
        for doc in documents
    ]
    
    client.upsert(
        collection_name=collection_name,
        points=points
    )

def retrieve_similar_documents(query_text, collection_name, top_k=5):
    query_vector = get_embedding(query_text)
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload['text'] for hit in search_results]

if __name__ == "__main__":
    documents = [
        {"id": 1, "text": "Sample text for training."},
        {"id": 2, "text": "Another training example."},
    ]

    insert_do