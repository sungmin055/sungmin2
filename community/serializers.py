from rest_framework import serializers
from .models import User, Post, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()  # 동적으로 계산되는 필드 추가
    author = UserSerializer()  # User 정보를 포함하도록 수정

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'image', 'like_count']
    
    def get_like_count(self, obj):
        # Post 모델의 like_count 메서드를 사용하여 좋아요 수 계산
        return obj.like_count()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # User 정보를 포함하도록 수정

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
