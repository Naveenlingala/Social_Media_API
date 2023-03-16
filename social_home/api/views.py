from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models
from .serializers import PostsSerializer, LikeSerializer

class ViewPosts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Post.objects.all()
    serializer_class = PostsSerializer


class LikePosts(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    # Override Post     
    def post(self, request, pk):
        post = models.Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user
        like = models.Like.objects.filter(user=user, post=post).first()
        if like is not None:
            return Response({'error': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post)
        return Response({'detail': 'successful'}, status=status.HTTP_201_CREATED)


class UnlikePosts(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    # Override destroy
    def perform_destroy(self, instance):
        instance.delete()

    # Override delete
    def delete(self, request, pk):
        post = models.Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        like = models.Like.objects.filter(post=post, user=request.user).first()
        if like is None:
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(like)
        self.get_serializer(post)
        return Response({'detail': 'successful'}, status=status.HTTP_200_OK)


