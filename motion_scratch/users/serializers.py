from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import FriendRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    total_followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'total_followers']
        #exclude = ['password']

    def get_total_followers(self, user):
        return user.followed_by.count()


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = '__all__'
        many = True


class AcceptedFriends(serializers.ModelSerializer):
    receiver = UserSerializer(required=False)

    class Meta:
        model = FriendRequest
        fields = ['receiver']
        many = True
