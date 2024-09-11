from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializer import UserSerializer,UserProfileSerializer
from .models import User
from rest_framework.views import APIView

class UserView(APIView):
        
    def get(self, request):
        user = get_object_or_404(User, email=request.user)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                serializer.initial_data["email"],
                serializer.initial_data["username"],
                serializer.initial_data["password"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
