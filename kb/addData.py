import pinecone
from sentence_transformers import SentenceTransformer
import json
import streamlit as st

# Initialize Pinecone and the Instructor model
pinecone.init(api_key=st.secrets["general"]["PINECONEAPIKEY"], environment="us-east-1")
index_name = "restaurant-index"

# Create a Pinecone index (if it doesn't already exist)
# Assuming 512-dimensional embeddings for `hkunlp/instructor-large`
# pinecone.create_index(index_name, dimension=512)  # Or 768 depending on your model's output size
index = pinecone.Index(index_name)

# Initialize the Instructor model from Hugging Face
instructor_embeddings = SentenceTransformer('hkunlp/instructor-large')
# Load restaurant data from a JSON file
with open('restaurant_data.json', 'r') as file:
    restaurant_data = json.load(file)

# Function to convert restaurant data into embeddings
def generate_embeddings(data):
    texts = [f"{item['Item Name']} {item['Category']} {item['Description']}" for item in data]
    embeddings = instructor_embeddings.encode(texts, convert_to_tensor=True)
    return embeddings

# Function to upsert data into Pinecone
def upsert_data_to_pinecone(data, embeddings):
    upserted_data = []
    for i, item in enumerate(data):
        # Use a unique ID for each item, for example, using the index
        vector_id = str(i)
        metadata = {
            "Restaurant": item["Restaurant"],
            "Item Name": item["Item Name"],
            "Category": item["Category"],
            "Veg/NonVeg": item["Veg/NonVeg"],
            "Price": item["Price"],
            "Description": item["Description"]
        }
        upserted_data.append((vector_id, embeddings[i], metadata))

    # Upsert the vectors into Pinecone
    index.upsert(vectors=upserted_data)

# Function to query Pinecone for similar items
def query_pinecone(query, top_k=5):
    # Generate an embedding for the user's query
    query_embedding = instructor_embeddings.encode([query], convert_to_tensor=True)[0]
    
    # Perform similarity search in Pinecone
    result = index.query([query_embedding], top_k=top_k, include_metadata=True)
    
    return result

# Generate embeddings for the restaurant menu items
embeddings = generate_embeddings(restaurant_data)

# Upsert the data into Pinecone
upsert_data_to_pinecone(restaurant_data, embeddings)
