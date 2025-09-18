from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        """
        示例 RAG pipeline，你可以替换为自己的实现
        """
        # 1. 检索（伪代码）
        docs = ["示例文档片段1", "示例文档片段2"]

        # 2. 大模型生成（伪代码）
        answer = f"这是基于 RAG 的回答，问题是：{query}"

        return {"answer": answer, "docs": docs}