from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..RAG.retriever import retrieve_from_vector_database
# Create your views here.


class ChatAPIView(APIView):
    """
    RAG 文字交互 API
    """

    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 这里调用你的 RAG pipeline
        # 假设 rag_pipeline 返回 {"answer": "...", "docs": ["...","..."]}
        result = self.rag_pipeline(user_query)

        return Response(result)

    def rag_pipeline(self, query: str) -> dict:
        answer = retrieve_from_vector_database(query)
        return {"reply" : answer}