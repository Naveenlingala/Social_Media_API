from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('authenticate', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('posts', views.ViewPosts.as_view()),
    path('like/<int:pk>', views.LikePosts.as_view()),
    path('unlike/<int:pk>', views.UnlikePosts.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
