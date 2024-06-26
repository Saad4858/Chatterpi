import chromadb
import PyPDF2
import os
import pickle

chroma_client = chromadb.Client()

# import the embeddings and the IDs from the .pkl file
with open('chroma/embeddings.pkl', 'rb') as file:
    ids, embeddings, documents = pickle.load(file)
    
# Create a new collection
collection = chroma_client.create_collection(name="col_chatterpi")

# Add the embeddings and the IDs to the new collection
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=documents
)

# perform any queries on the collection

def query_collection(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results



