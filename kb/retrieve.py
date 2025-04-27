from langchain.embeddings import HuggingFaceInstructEmbeddings
from pinecone import Pinecone
import streamlit as st

# pineconeAPIKey = st.secrets["PINECONEAPIKEY"]

# pc = Pinecone(api_key=pineconeAPIKey)

# indexName = "riccardo"
# index = pc.Index(indexName)

# instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

def retrieve_resto_data(question):
    # """
    # Simulate fetching restaurant data based on the query.
    # In reality, this would query a vector database like FAISS, Chroma, etc.
    # """

    # e = instructor_embeddings.embed_query(question)

    # data = index.query(
    # vector = e,
    # top_k = 5,
    # include_values = True
    # )

    # matches = data['matches']  # Get all matches
    # # Extract IDs from the first 3 matches
    # prompts_responses = []

    # for match in matches[:2]:
    #     extracted_id = int(match['id'])
    #     print("Extracted ID:", extracted_id)

    #     prompt = None
    #     response = None

    #     try:
    #         fetch = index.fetch([str(extracted_id)]) 
    #         prompt = fetch['vectors'][str(extracted_id)]['metadata']['prompt']
    #         response = fetch['vectors'][str(extracted_id)]['metadata']['resource']
    #         # Append prompt and response (if available) to the list
    #         if prompt is not None and response is not None:
    #             prompts_responses.append((prompt, response))
    #         else:
    #             print("No row")
    #     except:
    #         print("Error")

    return [
            {
                "name": "Mcdonald",
                "cuisine": "Italian",
                "location": "Downtown",
                "rating": 4.6,
                "menu": [
                    {"item": "Margherita Pizza", "price": "$12"},
                    {"item": "Pasta Alfredo", "price": "$14"},
                    {"item": "Tiramisu", "price": "$8"},
                    {"item": "Bruschetta", "price": "$7"}
                ],
                "timings": "11 AM - 11 PM",
                "specialties": "Authentic wood-fired pizzas and homemade pastas"
            },
            {
                "name": "Royal Cafe",
                "cuisine": "Japanese",
                "location": "Uptown",
                "rating": 4.8,
                "menu": [
                    {"item": "Salmon Nigiri", "price": "$10"},
                    {"item": "California Roll", "price": "$9"},
                    {"item": "Miso Soup", "price": "$5"},
                    {"item": "Tempura Udon", "price": "$13"}
                ],
                "timings": "12 PM - 10 PM",
                "specialties": "Fresh sushi and traditional Japanese noodle soups"
            }
        ]