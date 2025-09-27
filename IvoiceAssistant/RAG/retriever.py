from .chroma_db_init import chromadb_client, chromadb_collection, cross_encoder, embedding_model, embed_chunk
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

def retrieve_from_vector_database(query: str) -> list[str]:

    client = OpenAI(api_key=os.getenv('DeepSeek_API_Key'), base_url="https://api.deepseek.com")

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

    message = [
            {
                "role": "system",
                "content": """你是一位专业的知识助手，名字叫做小王，需要根据提供的相关文档片段来回答用户问题。

        请严格遵守以下规则：
        1. 只使用提供的相关片段中的信息回答问题
        2. 如果片段中没有相关信息，请明确告知"根据现有资料无法回答该问题"
        3. 可以适当根据片段内容进行合理推测和总结，如：美国报销=其他大洲报销
        4. 保持回答准确、简洁和专业"""
            },
            {
                "role": "user",
                "content": f"""用户问题：{query}

        相关文档片段：
        {retrieved_chunks}

        请基于以上片段内容回答用户问题。"""
            },
        ]
    #print(message)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        stream=False
    )

    return response.choices[0].message.content
