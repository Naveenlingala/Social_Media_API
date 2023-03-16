from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    # JWT
    path('authenticate', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('all_posts', views.ViewPosts.as_view(), name='post_list'),
    path('like/<int:pk>', views.LikePosts.as_view(), name='like'),
    path('unlike/<int:pk>', views.UnlikePosts.as_view(), name='unlike'),
    path('follow/<int:pk>', views.FollowUser.as_view(), name='follow'),
    path('unfollow/<int:pk>', views.UnfollowUser.as_view(), name='unfollow'),
    path('posts/', views.CreatePostView.as_view(), name="post_create"),
    path('user', views.UserDetails.as_view(), name='user_details'),
    path('posts/<int:pk>', views.DeletePostView.as_view(), name="post_delete"),
    path('comment/<int:pk>', views.CreateCommentView.as_view(), name='comment'),
]
