from django.db.models import Q
from rest_framework import filters

# Create your views here.

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Comments

from posts.permissions import IsOwnerOfPostOrReadOnly
from posts.serializers import PostSerializer, CommentsSerializer
from users.models import User, FriendRequest


# creates post
class CreatePost(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = Post(owner=self.request.user, **serializer.validated_data)
        post.save()


# gets the post by id
class ListCreatePosts(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'title']


# deletes or updates the post by id
class GetDeleteUpdatePostView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_id'
    permission_classes = [IsAuthenticated, IsOwnerOfPostOrReadOnly]


# get all posts from one user     this code gets read, not executed. Only def method gets executed
class GetPostsOfUser(ListAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = 'owner_id'
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        owner = User.objects.get(id=owner_id)
        posts = owner.posts.all().order_by('timestamp').reverse()    # this returns instances

        return posts


# lists all the posts of followed users in chronological order
class GetPostsOfFollowedUsers(GenericAPIView):
    def get(self, request):
        user = self.request.user
        posts = Post.objects.filter(owner__in=user.i_follow.all()).order_by('timestamp').reverse()
        serializer = PostSerializer(instance=posts, many=True)
        return Response(serializer.data)


# list posts of friends in chronological order
class GetPostsOfFriends(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        requested_friend_requests = FriendRequest.objects.filter(Q(requester=self.request.user, status='accepted'))
        # this loop goes through all the user IDs and extracts them from my accepted friend requests
        requested_friend_requests_ids = [friend_request.receiver.id for friend_request in requested_friend_requests]

        received_friend_requests = FriendRequest.objects.filter(Q(receiver=self.request.user, status='accepted'))
        received_friend_requests_id = [friend_request.requester.id for friend_request in received_friend_requests]

        user_ids = requested_friend_requests_ids + received_friend_requests_id
        return Post.objects.filter(owner_id__in=user_ids)


# noinspection DuplicatedCode
class ToggleLike(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    # the method which likes or unlikes the post
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.liked_by.all():    # "all" gets all the users, and request.user checks is it is
            post.liked_by.remove(request.user)     # already liked by that particular user
        else:
            post.liked_by.add(request.user)
        return Response(self.get_serializer(instance=post).data)


# get the list of the posts liked by user
class LikedByUser(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(liked_by=self.request.user)


class ListCreateComments(ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'post_id'

    # Creates new comment on a post
    def perform_create(self, serializer):
        post = self.kwargs['post_id']
        comment = Comments(owner=self.request.user, post_id=post, **serializer.validated_data)
        comment.save()

        # Override get_queryset method to list all comments of a post in reverse chronological order
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post=Post.objects.get(id=post_id)
        comments = post.comments.all().order_by('timestamp').reverse()  # this returns instances
        return comments
