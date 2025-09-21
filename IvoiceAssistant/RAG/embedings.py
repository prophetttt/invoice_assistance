from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
from .chroma_db_init import chromadb_client, chromadb_collection, cross_encoder, embedding_model, embed_chunk

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


    chunks = split_into_chunks_file("/Users/zhangyifu/Documents/RAG/old_invoice/library.md")
    save_embeddings(chunks, embed_chunk(chunks))