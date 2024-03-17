import pandas as pd
import numpy as np
import embeds

# Load the embedded data
embedded_df = pd.read_csv('embedded.csv')
embeddings = np.array(embedded_df['ada_embedding'].to_list())

# Function to find the closest embedding to a given query
def find_closest_embedding(embeddings, query):
    # When given a query converts the query into an embedding
    query_embedding = embeds.get_embedding(query, model='text-embedding-3-small')

    # Calculates cosine similarity scores between query embedding and all embeddings
    similarities = np.dot(embeddings, query_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding))

    # Find index of maximum similarity score
    max_index = np.argmax(similarities)
    return max_index, similarities[max_index]