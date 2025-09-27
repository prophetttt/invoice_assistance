from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
chromadb_client = chromadb.PersistentClient(path="./chroma_db")
chromadb_collection = chromadb_client.get_or_create_collection(name="default")


cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")


def embed_chunk(chunk: str) -> list[float]:
    embedding = embedding_model.encode(chunk, normalize_embeddings=True)
    return embedding.tolist()