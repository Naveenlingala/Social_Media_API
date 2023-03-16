from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followers')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='following')

    @property
    def username(self):
        return f'{self.user.username}'
    
    @property
    def number_of_followers(self):
        return self.followers.count()
    
    @property
    def number_of_following(self):
        return self.following.count()

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=3000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def post_comments(self):
        list_comments = []
        for comment in self.comments.all():
            list_comments.append({"author":comment.author(), "content": comment.text})
        return list_comments
    
    @property
    def total_likes(self):
        return self.likes.count
    
    class Meta:
        unique_together = ('title', 'description')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=408, blank=False)

    class Meta:
        unique_together = ('user', 'text')
        
    def author(self):
        return f'{self.user.username}'

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')