import chromadb
import PyPDF2
import os
import pickle

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="col_chatterpi")

# Initialize an empty list to store all the text
all_text = []

# Specify the directory where the PDFs are
pdf_dir = 'pdf_pool'

# Loop through each file in the directory
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        # Open the PDF file
        with open(os.path.join(pdf_dir, filename), 'rb') as file:
            # Create a PDF file reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Loop through each page in the PDF
            for page in pdf_reader.pages:
                # Extract the text from the page
                page_text = page.extract_text()

                # Append the text to the list
                all_text.append(page_text)

# Now all_text contains the text of all PDFs in the directory

# for each string in the list all_text, split the string into a list of sentences on . or ? or !
# add all these sentences to the collection
for i, text in enumerate(all_text):
    sentences = text.split(".")
    sentences = [sentence.strip() for sentence in sentences]
    collection.add(
        ids=[str(i) + "_" + str(j) for j in range(0, len(sentences))],  # IDs are just strings
        documents=sentences,
        metadatas=[{"type": "support"} for _ in range(0, len(sentences))],
    )
    
    
    
# import the questions from the questions.txt file
# with open('chroma/questions.txt', 'r') as file:
#     questions = file.readlines()
    
# remove the newline character from each question
# questions = [question.strip() for question in questions]
        
# results = collection.query(
#     query_texts=questions,
#     n_results=1)

# # Print the question and the corresponding support
# for i, q in enumerate(questions):
#     print(f"Question: {q}")
#     print(f"Retrieved support: {results['documents'][i][0]}")
#     print()
    
# export the collection to a .pkl file
ids = collection.get()['ids']
embeddings = collection.get(include=['embeddings'])['embeddings']
documents = collection.get(include=['documents'])['documents']

# Save the embeddings and the IDs to a .pkl file
with open('chroma/embeddings.pkl', 'wb') as file:
    pickle.dump((ids, embeddings, documents), file)