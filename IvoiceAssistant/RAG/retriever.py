from .chroma_db_init import chromadb_client, chromadb_collection, cross_encoder, embedding_model, embed_chunk
def retrieve_from_vector_database(query: str) -> list[str]:
    def retrieve(query: str, top_k: int) -> list[str]:
            query_embedding = embed_chunk(query)
            results = chromadb_collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results['documents'][0]
    def rerank(query: str, retrieved_chunks: list[str], top_k: int) -> list[str]:
        pairs = [(query, chunk) for chunk in retrieved_chunks]
        scores = cross_encoder.predict(pairs)

        scored_chunks = list(zip(retrieved_chunks, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return [chunk for chunk, _ in scored_chunks][:top_k]


    retrieved_chunks = retrieve(query, 5)
    retrieved_chunks = rerank(query, retrieved_chunks, 3)
    return retrieved_chunks