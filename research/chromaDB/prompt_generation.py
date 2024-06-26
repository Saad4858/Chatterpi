# Import
import chromadb
import pandas as pd
import numpy as np
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Read the CSV file
df = pd.read_csv('Crop_recommendation.csv')

# Shuffling Data
df = df.sample(frac=1)

# Splitting Data In Half, 50/50 split
split_index = int(df.shape[0] / 2.0)
print(split_index)
df_part1 = df.iloc[:split_index]
df_part2 = df.iloc[split_index:]

# Model Name
model_name = "all-mpnet-base-v2" # Change Embedding Model Here

# Saving First Half of DataFrame For Testing
test_csv = "crop_recommendation_For_Testing_embed_" + model_name + ".csv"
df_part1.to_csv(test_csv, index=False)

# Using Other half as context store in ChromaDB
context_csv = "crop_recommendation_For_Context_embed_" + model_name + ".csv"
df_part2.to_csv(context_csv, index=False)

# Extracting First 7 Columns as Rows of Context Store Data
df = pd.read_csv(context_csv)

first_seven_columns = df.iloc[:, :-1]

# Extracting Gold Labels
last_eighth_column = df.iloc[:, -1]

first_seven_columns = np.array(first_seven_columns)

last_eighth_column = np.array(last_eighth_column)

# String Conversion of Soil Measures
concatenated_strings = [','.join(map(str, sublist)) for sublist in first_seven_columns]

# Chroma Client
chroma_client = chromadb.Client()
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
collection = chroma_client.create_collection(name="TestCollection", embedding_function=sentence_transformer_ef)

# Readying MetaData With Crop Gold Labels
meta = []

for data in last_eighth_column:
  d = {"source": f"{data}"}
  meta.append(d)

# Adding To Collection
collection.add(
    documents=concatenated_strings,
    metadatas=meta,
    ids=[str(i) for i in range(1, 1101)]
)

# Retreiving Test Data
df = pd.read_csv(test_csv)

test_rows = df.iloc[:, :-1]

# Extracting Gold Labels
test_labels = df.iloc[:, -1]

test_rows = np.array(test_rows)

test_labels = np.array(test_labels)

# String Conversion
data_strings_test = [','.join(map(str, sublist)) for sublist in test_rows]

# Retreiving Top Three Matches From Collection
prompts = []

for row in data_strings_test:
  results = collection.query(
      query_texts=[row],
      n_results=3,
  )

  # Extracting Crop from Results
  crops = []
  for data in results['metadatas']:
    for dictionary in data:
      crops.append(dictionary['source'])

  # Extracting Documents From Results
  labels = ['Nitrogen Content', 'Phosphorous Content', 'Potassium Content',
            'Temperature', 'Humidity', 'pH', 'Rainfall']

  labeled_data = []
  for docs in results['documents']:
    for doc in docs:
      values = doc.split(',')
      transformed_data = ', '.join(f'{label}: {value}' for label, value in zip(labels, values))
      labeled_data.append(transformed_data)

  # Making Our Prompt
  prompt = "Given the following:"
  for i in range(3):
    prompt = prompt + '\n' + labeled_data[i] + ", Plant " + crops[i]

  values = row.split(',')
  transformed_row = ', '.join(f'{label}: {value}' for label, value in zip(labels, values))

  prompt = prompt + "\n What is the ideal crop to plant for the following conditions: " + transformed_row

  prompts.append(prompt)

# Adding Prompts to CSV File For Storage
df = pd.DataFrame(prompts, columns=['Prompts_with_Context'])

df['Labels'] = test_labels
df

# Writing to a CSV File

csv_name = "Context_Prompts_embed_" + model_name + ".csv"
df.to_csv(csv_name, index=False)

#chroma_client.delete_collection(name="TestCollection")