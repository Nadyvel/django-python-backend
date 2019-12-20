from rest_framework import serializers
from users.serializers import UserSerializer

from posts.models import Post, Comments


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    total_likes = serializers.SerializerMethodField()  # searches for a function which is called get_total_likes and executes it

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['owner']

    def get_total_likes(self, post):
        return post.liked_by.count()   # gives all the relations and the amount of likes for the post


class CommentsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['owner']