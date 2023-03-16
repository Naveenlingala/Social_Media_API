from rest_framework import serializers

from . import models

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = [
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



        
    