from rest_framework import serializers

from . import models

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'total_likes',
            'post_comments'
        ]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = []


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = []

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.UserProfile
        fields = [
            'username',
            'number_of_followers',
            'number_of_following',
        ]       

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = [
            'id', 
            'title', 
            'description', 
            'created_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            'text'
        ]