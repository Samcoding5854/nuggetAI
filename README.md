# Restaurant Data Scraper & RAG-based Chatbot

## Overview

In this project, we combine web scraping with a Retrieval Augmented Generation (RAG) chatbot to enhance the user experience of restaurant platforms, such as Zomato. The solution allows customers to ask natural language questions about restaurants and receive accurate, contextual responses based on up-to-date information scraped from restaurant websites.

### Problem Statement

Users often have specific questions about restaurants that are not easily answered through traditional search, such as:

- "Which restaurant has the best vegetarian options in their menu?"
- "Does ABC restaurant have any gluten-free appetizers?"
- "What's the price range for XYZ restaurant's dessert menu?"
- "Compare the spice levels mentioned in the menus of restaurants A and B."

This project aims to answer these types of questions by:

1. Collecting real restaurant data through web scraping
2. Processing and storing this information appropriately
3. Building a RAG-based chatbot that retrieves relevant information and generates helpful responses

## Technologies Used

- **Python**: The main programming language for implementing the entire solution.
- **Streamlit**: For the user interface (UI), enabling an interactive environment for users to interact with the chatbot.
- **Pinecone**: A vector database to store restaurant data embeddings for efficient retrieval.
- **HuggingFace's Instructor Model**: To generate embeddings for restaurant data and user queries.
- **BeautifulSoup**: For web scraping restaurant data from websites.
- **Sentence-Transformers**: To convert text data into vector representations using the `hkunlp/instructor-large` model.
- **Pinecone Client**: To store and retrieve vector embeddings from the Pinecone database.

## Project Structure

```
.
├── .streamlit/
│   └── secrets.toml
├── assets/
├── kb/
│   ├── __init__.py
│   ├── addData.py
│   ├── convert_data.py
│   └── retrieve.py
├── prompts/
│   └── prompts.py
├── scraper/
│   ├── checking.py
│   └── spider.py
├── .gitignore
├── app.py
├── README.md
├── requirements.txt
```

## Requirements

Make sure to install the required dependencies using `pip`. You can create a virtual environment and install the dependencies as follows:

```bash
pip install -r requirements.txt
```

### `requirements.txt`:

```plaintext
pinecone-client
sentence-transformers
streamlit
beautifulsoup4
requests
```

## Setup

1. **Initialize Pinecone**: Set up a Pinecone index to store the vector embeddings.

```python
import pinecone

pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-west1-gcp")
pinecone.create_index(index_name="restaurant-index", dimension=512)  # or 768
```

2. **Run the Web Scraper**: The web scraper extracts restaurant data such as name, menu items, descriptions, prices, and special features (e.g., vegetarian options, spice levels). It organizes the data into a structured format suitable for retrieval. To run the scraper, use the following command:

To scrape restaurant data, use the following command:

```bash
python scraper/spider.py <URL>
```

Replace `<URL>` with the Zomato restaurant URL you want to scrape. For example:

```bash
python scraper/spider.py https://www.zomato.com/mumbai/rasoi-dadar-east
```

#### Explanation:

- **URL Format**: Provide the full Zomato restaurant URL in the command.
- **Example URL Format**: `https://www.zomato.com/<city>/<restaurant-name>`

For instance, to scrape data from the restaurant "Rasoi" in Mumbai, the URL would be:

```plaintext
https://www.zomato.com/mumbai/rasoi-dadar-east
```

3. **Generate Embeddings**: Use HuggingFace's `Instructor` model to generate embeddings for both restaurant data and user queries.

```python
from sentence_transformers import SentenceTransformer

instructor_embeddings = SentenceTransformer('hkunlp/instructor-large')

def generate_embeddings(texts):
    embeddings = instructor_embeddings.encode(texts, convert_to_tensor=True)
    return embeddings
```

4. **Store Data in Pinecone**: Once you have the embeddings for the restaurant data, you can upsert the embeddings into Pinecone.

```python
import pinecone

def upsert_to_pinecone(data, embeddings):
    upserted_data = []
    for i, item in enumerate(data):
        vector_id = str(i)
        metadata = {
            "Restaurant": item["Restaurant"],
            "Item Name": item["Item Name"],
            "Category": item["Category"],
            "Price": item["Price"],
            "Description": item["Description"]
        }
        upserted_data.append((vector_id, embeddings[i], metadata))
    index = pinecone.Index("restaurant-index")
    index.upsert(vectors=upserted_data)
```

5. **Build the RAG-based Chatbot**: The chatbot will retrieve relevant information from the Pinecone index and generate natural language responses using HuggingFace’s models.

```python
def query_pinecone(query):
    query_embedding = instructor_embeddings.encode([query], convert_to_tensor=True)[0]
    result = index.query([query_embedding], top_k=5, include_metadata=True)
    return result
```

6. **User Interface with Streamlit**: Create an interactive UI where users can input queries and receive responses.


### Running the Streamlit App

To start the Streamlit app, run the following command:

```bash
streamlit run app.py
```

This will launch the Streamlit app in your browser, allowing users to ask questions about restaurants and receive relevant responses.

## Features

- **Web Scraping**: Extract restaurant information, including menu items, descriptions, and pricing.
- **Retrieval-Augmented Generation (RAG)**: Leverages Pinecone's vector search and HuggingFace's language models to generate responses.
- **Interactive Chatbot UI**: Users can ask questions through a simple Streamlit app and get answers.
- **Custom Query Types**: The chatbot handles different types of queries, including menu item availability, restaurant feature comparisons, price range, and dietary restriction questions.

## How It Works

1. **Scrape Restaurant Data**: Scrape the restaurant menus, including item names, prices, descriptions, and special features like vegetarian options and allergens.
2. **Generate Embeddings**: Convert the text data into vector embeddings using the HuggingFace `Instructor` model.
3. **Store Data in Pinecone**: Store these embeddings in the Pinecone vector database for fast retrieval.
4. **Query Handling**: When the user asks a question, the system converts the query into an embedding and searches the Pinecone database for the most relevant menu items.
5. **Answer Generation**: The system retrieves the most relevant data and presents it in a user-friendly format.

## Future Improvements

- **Better Query Handling**: Implement more sophisticated NLP techniques for better understanding of ambiguous queries.
- **Web Scraper Enhancements**: Extend the scraper to handle more diverse restaurant website structures and include additional data such as operating hours and contact details.
- **User Feedback**: Add a feedback loop for users to rate the responses, helping to refine and improve the system.

## Conclusion

This project simulates a real-world application of enhancing user interaction with restaurant data through a chatbot that uses web scraping, a knowledge base, and RAG-based retrieval and generation techniques. The result is a conversational AI system that can answer detailed and contextually relevant questions about restaurants.

---

### Key Additions:
- **Streamlit UI**: Streamlit was added to provide an interactive interface for users to interact with the chatbot.
- **Embeddings and Pinecone Integration**: The use of Pinecone to store and query vector embeddings ensures fast and efficient retrieval of restaurant information.
- **Model-based Question Answering**: The `Instructor` model from HuggingFace generates embeddings for both data and user queries.
