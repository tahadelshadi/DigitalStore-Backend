
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name')
    class Meta:
        model = Comment
        fields = ['user','context','rate','created_at']
    