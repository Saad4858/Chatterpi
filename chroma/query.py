import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from get_embeddings  import query_collection


results =query_collection("What is one way to measure efficency of land area ?")
documents = results['documents'][0]

for i in documents:
    print(i)
    print('\n')





    











