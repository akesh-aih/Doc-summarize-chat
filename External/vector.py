import os
from aih_rag.schema import TextNode
from aih_rag.vector_stores.deeplake import DeepLakeVectorStore
from aih_rag.vector_stores.types import VectorStoreQuery, VectorStoreQueryResult

class DeepLakeManager:
    def __init__(self, dataset_path, overwrite=True, ingestion_batch_size=10, ingestion_num_workers=2, verbose=False):
        # Initialize the DeepLake vector store
        self.vector_store = DeepLakeVectorStore(
            dataset_path=dataset_path,
            overwrite=overwrite,
            ingestion_batch_size=ingestion_batch_size,
            ingestion_num_workers=ingestion_num_workers,
            verbose=verbose
        )

    def add_nodes(self, nodes):
        # Add nodes to DeepLake vector store
        added_node_ids = self.vector_store.add(nodes)
        # print(f"Added nodes with IDs: {added_node_ids}")
        return added_node_ids

    def query_store(self, query_embedding, top_k=3):
        # Query the vector store with the provided embedding
        query = VectorStoreQuery(query_embedding=query_embedding, similarity_top_k=top_k)
        results = self.vector_store.query(query=query)
        queried_texts = [node.text for node in results.nodes]
        # print(f"Queried Texts: {queried_texts}")
        return queried_texts

# User-defined functions to interact with the class

def initialize_store():
    dataset_path = os.path.join(os.getcwd(), "deeplake_dataset")  # Example dataset path
    manager = DeepLakeManager(dataset_path=dataset_path)
    return manager

import uuid

def add_custom_nodes(manager, text_list, embedding_list):
    """
    Adds nodes to the vector store with UUIDs as node IDs, based on user-provided text and embedding.
    
    :param manager: Instance of the DeepLakeManager.
    :param text_list: List of texts to be added.
    :param embedding_list: Corresponding list of embeddings for the texts.
    """
    if len(text_list) != len(embedding_list):
        raise ValueError("The number of texts and embeddings must be the same.")

    nodes = []
    for text, embedding in zip(text_list, embedding_list):
        node_id = str(uuid.uuid4())  # Generate a unique ID for each node
        node = TextNode(node_id=node_id, text=text, embedding=embedding)
        nodes.append(node)

    manager.add_nodes(nodes)
    # print(f"Added {len(nodes)} nodes to the vector store.")

def query_custom_embedding(manager, query_embedding):
    """
    Queries the vector store with a user-provided embedding.
    
    :param manager: Instance of the DeepLakeManager.
    :param query_embedding: The embedding to be used for querying.
    """
    results = manager.query_store(query_embedding=query_embedding)
    return results
# Example usage
# if __name__ == "__main__":
#     # Step 1: Initialize the store
#     manager = initialize_store()

#     # Step 2: Add sample nodes
#     add_sample_nodes(manager)

#     # Step 3: Query the store
#     query_sample(manager)
