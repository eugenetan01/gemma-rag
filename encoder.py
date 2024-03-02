from sentence_transformers import SentenceTransformer
import mongo_conn

# Load Dataset
from datasets import load_dataset
import pandas as pd

# https://huggingface.co/thenlper/gte-large
embedding_model = SentenceTransformer("thenlper/gte-large")

# https://huggingface.co/datasets/AIatMongoDB/embedded_movies
dataset = load_dataset("AIatMongoDB/embedded_movies")

# Convert the dataset to a pandas DataFrame
dataset_df = pd.DataFrame(dataset["train"])

# Remove data point where plot column is missing
dataset_df = dataset_df.dropna(subset=["fullplot"])
print("\nNumber of missing values in each column after removal:")
print(dataset_df.isnull().sum())

# Remove the plot_embedding from each data point in the dataset as we are going to create new embeddings with an open-source embedding model from Hugging Face: gte-large
dataset_df = dataset_df.drop(columns=["plot_embedding"])


def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []
    embedding = embedding_model.encode(text)
    return embedding.tolist()


dataset_df["embedding"] = dataset_df["fullplot"].apply(get_embedding)

documents = dataset_df.to_dict("records")
collection = mongo_conn.get_mongo_coll()

# Delete any existing records in the collection
collection.delete_many({})

collection.insert_many(documents)
print("Data ingestion into MongoDB completed")
