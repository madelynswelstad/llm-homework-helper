import os
import fitz  # PyMuPDF
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from dotenv import load_dotenv, find_dotenv
import speech_recognition as sr
import pyttsx3

# Load environment variables
_ = load_dotenv(find_dotenv())

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="https://071a9cd4-154f-4464-acfe-bb7a4ecb9770.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=os.environ['QDRANT_API_KEY']
)

# Define collection parameters
collection_name = 'llm_training_data'
vector_size = 1536  # Matches OpenAI's text-embedding-ada-002
distance_metric = Distance.COSINE

def find_collections(collectionName):
    collections_response = qdrant_client.get_collections()
    # Extract the list of collection names
    collection_names = [collection.name for collection in collections_response.collections]

    if collectionName in collection_names:
        print(f"Collection '{collectionName}' already exists.")
    else:
        create_collection(collectionName)

def create_collection(collection_name):
    """Create a collection in Qdrant if it doesn't already exist."""
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance_metric),
        )
        print(f"Collection '{collection_name}' created successfully.")
    else:
        print(f"Collection '{collection_name}' already exists. Skipping creation.")

def get_embedding(text):
    """Generate an embedding for the input text using OpenAI."""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def insert_documents(documents, collection_name):
    """Insert documents with embeddings into the Qdrant vector store."""
    print(f'documents recieved: {documents}')
    points = [
        PointStruct(
            id=doc['id'],
            vector=get_embedding(doc['text']),
            payload={"text": doc['text']}
        )
        for doc in documents
    ]
    
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"Inserted {len(documents)} documents into '{collection_name}'.")

def retrieve_similar_documents(query_text, collection_name=collection_name, top_k=5):
    """Retrieve similar documents from Qdrant."""
    query_vector = get_embedding(query_text)
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload['text'] for hit in search_results]

def get_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    paragraphs = []
    with fitz.open(pdf_path) as file:
        for page in file:
            text = page.get_text("text")
            paragraphs.extend([p.strip() for p in text.split("\n") if p.strip()])
    return paragraphs

def delete_collection(collection_name):
    """Delete a Qdrant collection if it exists."""
    if qdrant_client.collection_exists(collection_name):
        qdrant_client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")

def process_query(input_data):
    query_answer = retrieve_similar_documents(query_text=input_data, top_k=3)

    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai_client.chat.completion.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    prompt = f"""
        You need to format {query_answer} so that a human reader can understand it. Please answer in English.
        
        Begin {query_answer} with "oi oi oi, baka"

        You are acting as an AI assistant to human users who are students of any level of education, up to college graduate.
        The users will be able to upload educational materials and your job is to parse these documents and use your collected 
        knowledge base to provide an informed response to {input_data}. 

        You should focus on educating the users so that they learn how to apply any concepts explained by {query_answer} to similar problems.
        Do not simply give the answers to {input_data} if {input_data} asks for an answer. {query_answer} should provide an educational
        walkthrough on how to solve the problem.

        If {input_data} is only a couple of words, {query_answer} should be a request for more information.

        {query_answer} should be respectful and encouraging. If the user indicates in {input_data} that they are upset or frustrated, {query_answer}
        should give the user a supportive and kind response that aims to make them feel happier.

        {query_answer} should have a relatively professional but casual tone. Avoid making jokes or acting comedic in {query_answer}.
    """

    response = get_completion(prompt)

    return response

def speech_to_text():
    """
    Requires installing
        - pyaudio (pip install pyaudio)
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to you poopy")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        return query
    except (sr.UnknownValueError):
        return "unknown value error"
    except (sr.RequestError):
        return "request error???"

def text_to_speech(text, filename="aianswer.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

def split_into_chunks(text_list, chunk_size=300):
    """Split text into chunks with a maximum token size."""
    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in text_list:
        paragraph_length = len(paragraph.split())
        if current_length + paragraph_length > chunk_size:
            # Save the current chunk and reset
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(paragraph)
        current_length += paragraph_length

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def get_text_from_pdf(pdf_path, chunk_size=300):
    """Extract and split text from a PDF file."""
    paragraphs = []
    with fitz.open(pdf_path) as file:
        for page in file:
            text = page.get_text("text")
            paragraphs.extend([p.strip() for p in text.split("\n") if p.strip()])
    # Split paragraphs into chunks
    return split_into_chunks(paragraphs, chunk_size)


if __name__ == "__main__":
    # Path to the PDF file
    pdf_path = "./hw1.pdf"

    delete_collection(collection_name)
    print("after delete")

    # Extract text from the PDF
    text_chunks = get_text_from_pdf(pdf_path)
    print("after paragraphs")

    # Prepare documents for insertion
    documents = [{"id": i, "text": paragraph} for i, paragraph in enumerate(text_chunks, 1)]

    # Create the Qdrant collection
    create_collection(collection_name)

    print("after collection")

    # Insert documents into Qdrant
    insert_documents(documents, collection_name)

    print("after insert")

    # Test query
    query = "Who wrote the paper on Unmanned Aerial Vehicles?"  # Replace with your query
    results = retrieve_similar_documents(query, collection_name)

    print("after results")

    print("Top similar results:")
    for i, result in enumerate(results, 1):
        print(f"{i}: {result}")


