# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(
        verbose_name='email address',
        unique=True
    )

    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
    )

    birth_date = models.DateField(
        verbose_name='birth date',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.username}'

    followed_by = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='followers',
        blank=True
    )

    i_follow = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='ifollow',
        blank=True,
    )


class FriendRequest(models.Model):
    STATUS = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default='pending'
    )

    requester = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='requester',
        related_name='requested',
        blank=True,
        null=True,
        on_delete=models.CASCADE,   # if I delete the requester then all the friend requests for this user will be deleted with this feature
    )

    receiver = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='receiver',
        related_name='received',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f' ID: {self.id} / Requester: {self.requester}/ Receiver: {self.receiver}/ Status:{self.status}/'
