from django.db import models


# Create your models here.
from project import settings


class Post(models.Model):
    owner = models.ForeignKey(
        verbose_name='user',
        to=settings.AUTH_USER_MODEL,  # authentication of the user in the settings.py file
        on_delete=models.CASCADE,
        related_name='posts',  # reverse relation from user to post
        null=True
    )

    share_post = models.ForeignKey(
        verbose_name='shared post',
        to='self',
        on_delete=models.CASCADE,
        related_name='posts',  # reverse relation from user to post
        null=True,
        blank=True
    )
    title = models.TextField(
        verbose_name='title',
        blank=True,
        null=True
    )

    content = models.TextField(
        verbose_name='content'
    )

    timestamp = models.DateTimeField(
        verbose_name='timestamp',
        auto_now_add=True           # adds date and time automatically to the post.
    )
    postpic = models.ImageField(
        upload_to='',
        blank=True,
        null=True
    )
    external_link = models.TextField(
        verbose_name='link',
        blank=True
    )

    def __str__(self):
        return f'{self.owner} / {self.content}'

    # the like method many to many
    # many to many creates a new table which connects the posts to the user.
    liked_by = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='likes',
        blank=True
    )

    class Meta:
        ordering = ('-timestamp',)


class Comments(models.Model):

    comment = models.TextField(
        verbose_name='comment',
        blank=True,
    )

    post = models.ForeignKey(
        verbose_name='post',
        to=Post,
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True
    )

    owner = models.ForeignKey(
        verbose_name='owner',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True
    )

    def __str__(self):
        return f' ID: {self.ID} / Comment: {self.comment}/ Post: {self.post}/ User:{self.user}/'
