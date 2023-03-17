from django.urls import reverse
import pytz
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, UserProfile, Comment, Like
from datetime import datetime, timedelta


class PostTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user_test', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            title='Test Post', description='Test Description', user=self.user)

    def test_create_post(self):
        url = reverse('post_create')
        post_data = {
            'title': 'Test Title',
            'description': 'Test Description'
        }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, 'Test Title')

    def test_delete_post(self):
        url = reverse('post_delete', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Post.objects.count(), 0)

    def test_retrieve_post(self):
        url = reverse('post_list')
        # Make another post
        time_change_post = Post.objects.create(title='Test Time Post ',
                                               description='Test Time Description', user=self.user)
        # Change Time
        increased_datetime = datetime.utcnow() + timedelta(minutes=6)
        # naive to aware
        time_change_post.created_at = pytz.timezone(
            'UTC').localize(increased_datetime)
        time_change_post.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check post descending by created_at
        post_1, post_2 = response.data
        self.assertEqual(post_2['id'], self.post.id)
        self.assertEqual(post_2['title'], self.post.title)
        self.assertEqual(post_2['description'], self.post.description)
        self.assertGreater(post_1['created_at'], post_2['created_at'])

    def test_like_post(self):
        url = reverse('like', kwargs={'pk': self.post.id})
        self.client.force_login(self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.total_likes, 1)

    def test_unlike_post(self):
        url = reverse('unlike', kwargs={'pk': self.post.id})
        self.client.force_login(self.user)
        # Like the post
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.total_likes, 0)

    def test_add_comment(self):
        url = reverse('comment', kwargs={'pk': self.post.id})
        self.client.force_login(self.user)
        data = {'text': 'test comment text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        owner = Comment.objects.filter(
            id=response.data['comment_id']).first().user
        self.assertEqual(self.user, owner)


class UserTestCase(APITestCase):
    def setUp(self):
        # create a user and a profile
        self.user = get_user_model().objects.create_user(
            username='user_test_1', password='testpass')
        self.profile = UserProfile.objects.create(user=self.user)

        # create another user and profile
        self.user2 = get_user_model().objects.create_user(
            username='user_test_2', password='testpass')
        self.profile2 = UserProfile.objects.create(user=self.user2)

        # create a post by user2
        self.post = Post.objects.create(
            title='Test post', description='Test description', user=self.user2)

        self.client.force_authenticate(user=self.user)

    def test_user(self):
        url = reverse('user_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['number_of_followers'],
                         self.user.profile.number_of_followers)
        self.assertEqual(response.data['number_of_following'],
                         self.user.profile.number_of_following)

    def test_follow_user(self):
        # follow user2
        url = reverse('follow', kwargs={'pk': self.user2.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.profile.following.all())
        self.assertIn(self.user, self.profile2.followers.all())

    def test_unfollow_user(self):
        # make user1 follow user2
        self.profile.following.add(self.user2)
        self.profile2.followers.add(self.user)

        # unfollow user2
        url = reverse('unfollow', kwargs={'pk': self.user2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.user2, self.profile.following.all())
        self.assertNotIn(self.user, self.profile2.followers.all())
