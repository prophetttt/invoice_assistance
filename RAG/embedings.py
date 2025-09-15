from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import chromadb
from sentence_transformers import SentenceTransformer
def retrieve(query: str, top_k: int) -> list[str]:
        query_embedding = embed_chunk(query)
        results = chromadb_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results['documents'][0]

def save_embeddings(chunks: list[str], embeddings: list[list[float]]) -> None:
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chromadb_collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[str(i)]
            )

def split_into_chunks(doc_file: str) -> list[str]:
        with open(doc_file, 'r') as file:
            content = file.read()

        return [chunk for chunk in content.split("\n\n")]
def embed_chunk(chunk: str) -> list[float]:
        embedding = embedding_model.encode(chunk, normalize_embeddings=True)
        return embedding.tolist()
def rerank(query: str, retrieved_chunks: list[str], top_k: int) -> list[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks][:top_k]




if __name__ == "__main__":

    chunks = split_into_chunks("library.md")

    # for i, chunk in enumerate(chunks):
    #     print(f"[{i}] {chunk}\n")

    embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")

    embeddings = embed_chunk(chunks)
    chromadb_client = chromadb.EphemeralClient()
    chromadb_collection = chromadb_client.get_or_create_collection(name="default")

    save_embeddings(chunks, embeddings)

    query = "我在杭州请客户吃了一顿饭，但是没有开发票。我能报销吗？"
    retrieved_chunks = retrieve(query, 5)

    for i, chunk in enumerate(retrieved_chunks):
        print(f"[{i}] {chunk}\n")


    reranked_chunks = rerank(query, retrieved_chunks, 3)

    for i, chunk in enumerate(reranked_chunks):
        print(f"[{i}] {chunk}\n")


    load_dotenv()
    google_client = genai.Client()

    def generate(query: str, chunks: list[str]) -> str:
        prompt = f"""你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。

    用户问题: {query}

    相关片段:
    {"\n\n".join(chunks)}

    请基于上述内容作答，不要编造信息。"""

        print(f"{prompt}\n\n---\n")

        response = google_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    answer = generate(query, reranked_chunks)
    print(answer)


