from langchain.embeddings import HuggingFaceInstructEmbeddings
import pinecone
from sentence_transformers import SentenceTransformer   
import streamlit as st


# Initialize Pinecone and the Instructor model
pinecone.init(api_key="pcsk_5cmofB_RaUySQtvUR7Har81JCViz5sroJ8gr2VLrjgqWpNZGJyQeok2CnZRwLxhEEQ3WBD", environment="us-east-1")
index_name = "restaurant-index"


index = pinecone.Index(index_name)

# Initialize the Instructor model from Hugging Face
instructor_embeddings = SentenceTransformer('hkunlp/instructor-large')


def retrieve_resto_data(question):
    # """
    # Simulate fetching restaurant data based on the query.
    # In reality, this would query a vector database like FAISS, Chroma, etc.
    # """

    # Generate an embedding for the user's query
    query_embedding = instructor_embeddings.encode([question], convert_to_tensor=True)[0]
    
    # Perform similarity search in Pinecone
    results = index.query([query_embedding], top_k=5, include_metadata=True)
    

    # Append the results into a single structure
    retrieved_data = []
    for match in results['matches']:
        retrieved_data.append({
            "item": match['metadata']['Item Name'],
            "restaurant": match['metadata']['Restaurant'],
            "score": match['score']
        })

    # Convert the structure to a string format
    return str(retrieved_data)