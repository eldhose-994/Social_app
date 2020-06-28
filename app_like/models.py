from django.contrib.auth.models import User
from django.db import models


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Post(Timestamp):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posted')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    published_date_time = models.DateTimeField(null=True, blank=True)


class TagWeight(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="get_all_post_tags")
    weight = models.PositiveSmallIntegerField(default=1)


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="get_all_posted_images")
    image = models.ImageField(upload_to='photos/', default='')


class Reaction(Timestamp):
    react_choice = (
        ('Like', 'Like'),
        ('Dislike', 'Dislike'),
    )
    reaction = models.CharField(max_length=7, choices=react_choice)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='get_all_post_reaction')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_liked_dislike')

    class Meta:
        unique_together = ('post', 'user', 'reaction')

#
# class DisLike(models.Model ,Timestamp):
#
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
