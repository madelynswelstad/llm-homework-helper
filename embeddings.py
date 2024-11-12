from openai import OpenAI
from typing import List
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv
import json


_ = load_dotenv(find_dotenv())
open_ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def create_embeddings(text_chunks: List[str]):
    embeddings = []

    for chunk in text_chunks:
        response = open_ai_client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings)


def load_embeddings_and_texts(embeddings_path: str, texts_path: str):
    embeddings = np.load(embeddings_path, allow_pickle=True)
    with open(texts_path, 'r') as f:
        texts = json.load(f)
    return embeddings, texts
