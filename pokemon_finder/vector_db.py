import os

import faiss
import numpy as np


class FaissManager:
    def __init__(self, dimension, index_file=None):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.index_file = index_file
        if index_file is not None and os.path.exists(index_file):
            self.load_index(index_file)

    def add_vectors(self, vectors):
        vectors = self.assure_shape(vectors)
        """Add vectors to the index after normalizing them."""
        faiss.normalize_L2(vectors)
        self.index.add(vectors)

    def save_index(self, index_file=None):
        """Save the index to a file."""
        if index_file is not None:
            self.index_file = index_file
        if self.index is not None and self.index_file is not None:
            faiss.write_index(self.index, self.index_file)

    def load_index(self, index_file):
        """Load an index from a file."""
        self.index = faiss.read_index(index_file)

    def search(self, vectors, k):
        vectors = self.assure_shape(vectors)
        """Search the index for the k most similar vectors."""
        faiss.normalize_L2(vectors)
        return self.index.search(vectors, k)

    def assure_shape(self, vectors):
        if vectors.dtype != np.float32:
            vectors = vectors.astype("float32")

        if len(vectors.shape) == 1:
            vectors = vectors.reshape(1, -1)

        return vectors


if __name__ == "__main__":
    # Usage
    dimension = 128  # Dimension of the vectors
    index_file = "faiss_index.idx"  # Path to save the index

    # Initialize the FAISS manager
    faiss_manager = FaissManager(dimension)

    # Assuming you have your database vectors in db_vectors
    db_vectors = np.random.random((10000, dimension)).astype("float32")

    # Create an index and add vectors
    faiss_manager.create_index(db_vectors)

    # Save the index to a file
    faiss_manager.save_index(index_file)

    # Assume we have some query vectors
    query_vectors = np.random.random((10, dimension)).astype("float32")

    # Search for the top 5 similar vectors for each query vector
    k = 5
    D, I = faiss_manager.search(query_vectors, k)

    # Print the results
    for i, (distances, indices) in enumerate(zip(D, I)):
        print(f"Query {i}:")
        for rank, (score, index) in enumerate(zip(distances, indices)):
            print(f"  Rank {rank}: Index {index}, Score {score}")

    # If you need to load the index later
    faiss_manager.load_index(index_file)
