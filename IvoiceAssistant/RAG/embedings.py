from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
chromadb_client = chromadb.PersistentClient(path="./chroma_db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")


cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")


def generate_vector_database():
    
    def save_embeddings(chunks: list[str], embeddings: list[list[float]]) -> None:
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chromadb_collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[str(i)]
            )

    def split_into_chunks_file(doc_file: str) -> list[str]:
            with open(doc_file, 'r') as file:
                content = file.read()
            return [chunk for chunk in content.split("\n\n")]

    def split_into_chunks(content: str) -> list[str]:
            return content.split("\n\n")

    def embed_chunk(chunk: str) -> list[float]:
            embedding = embedding_model.encode(chunk, normalize_embeddings=True)
            return embedding.tolist()
    pass 

def retrieve_from_vector_database(query: str, top_k: int) -> list[str]:
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