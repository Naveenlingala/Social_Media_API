import datetime
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models
from .serializers import PostsSerializer, LikeSerializer, UserProfileSerializer, UserSerializer, PostCreateSerializer, CommentSerializer
from django.contrib.auth.models import User


class ViewPosts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user).order_by('created_at')


class LikePosts(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    # Override Post     
    def post(self, request, pk):
        post = models.Post.objects.filter(pk=pk).first()
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        like = models.Like.objects.filter(user=user, post=post).first()
        if like is not None:
            return Response({'error': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post)
        return Response({'detail': f"Post '{post.title}' is Liked by {user.username}"}, status=status.HTTP_201_CREATED)


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
        return Response({'detail': f"Post '{post.title}' is UnLiked by {request.user.username}"}, status=status.HTTP_200_OK)


class FollowUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def create_or_return_object(self, instance):
        try:
            instance.profile
        except:
            user_profile = models.UserProfile(user = instance)
            user_profile.save()

        return instance    

    def post(self, request, pk):

        follow_user = User.objects.filter(pk=pk).first()
        if follow_user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        #Create Porfile if not found
        follow_user = self.create_or_return_object(follow_user)
        auth_user = self.create_or_return_object(request.user)
        
        if follow_user == auth_user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if auth_user.profile.following.filter(id = follow_user.id).exists():
            return Response({'error': 'You are already following the user'}, status=status.HTTP_400_BAD_REQUEST)
        #Add followers
        follow_user.profile.followers.add(auth_user)
        #Add following
        auth_user.profile.following.add(follow_user)
        follow_user.save()

        return Response({'detail':'Follow successful'}, status=status.HTTP_200_OK)
    

class UnfollowUser(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def delete(self, request, pk):
        follow_user = User.objects.get(pk=pk)
        auth_user = request.user

        if follow_user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if follow_user == auth_user:
            return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if auth_user.profile.following.filter(id = follow_user.id).exists():
            #Add followers
            follow_user.profile.followers.remove(auth_user)
            #Add following
            auth_user.profile.following.remove(follow_user)
            follow_user.save()
        else:
            return Response({'error': 'You are not following the user'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail':'Unfollow successful'},status=status.HTTP_200_OK)
    

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user.profile
    

class CreatePostView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        post_data = response.data
        post_data["created_at"] = datetime.datetime.strptime(post_data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        return Response(post_data, status=status.HTTP_201_CREATED)

class DeletePostView(generics.RetrieveDestroyAPIView):
    queryset = models.Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"error":"You do not have permission to delete this post"}, status=status.HTTP_403_FORBIDDEN)
        super().delete(request, *args, **kwargs)
        return Response({"detail":"delete sucessful"}, status=status.HTTP_202_ACCEPTED)
    

class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
        
    def post(self, request, pk):
        post = models.Post.objects.get(pk=pk)
        if post is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            comment_id = serializer.save(user=self.request.user, post_id=pk).id
        except:
            return Response({'error': 'Comment already found'}, status=status.HTTP_208_ALREADY_REPORTED)
        return Response({"comment_id": comment_id}, status=status.HTTP_201_CREATED)