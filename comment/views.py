
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_list_or_404
from .serializers import CommentSerializer
from .models import Comment


class CommentList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,product_id):
        comment_list = get_list_or_404(Comment,product=product_id)
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)