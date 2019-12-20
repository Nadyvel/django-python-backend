# Create your views here.
from django.db.models import Q
from rest_framework import filters

from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView, \
    CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.permissions import IsOwnerOfPostOrReadOnly
from users.permissions import IsReceiverOfFriendRequestOrReadOnly
from users.serializers import UserSerializer, AcceptedFriends, FriendRequestSerializer

from users.models import User, FriendRequest


class ToggleFollow(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    # the method which follows or unfollows the post
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user in user.followed_by.all():    # "all" gets all the users, and request.user checks is it is
            user.followed_by.remove(request.user)     # already liked by that particular user
        else:
            user.followed_by.add(request.user)
        return Response(self.get_serializer(instance=user).data)


# users who follow me
class AllLoggedInUserFollowers(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        followed_by_people = self.request.user.followers.all()  # filter the users follow me
        return followed_by_people


# users who I follow
class PeopleLoggedInUserFollows(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        ifollow_people = self.request.user.i_follow.all()  # filter the users im following
        return ifollow_people


# list all the users and search users
class GetListOfUsers(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOfPostOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


# Get specific user profile
class GetSpecificUserById(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"


class CreateFriendRequest(CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfPostOrReadOnly]

    # creates a friend request
    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        request_exists = FriendRequest.objects.filter(
            Q(requester=self.request.user) & Q(receiver_id=user_id)
            | Q(receiver=self.request.user) & Q(requester_id=user_id)).exists()
        if not request_exists:
            friendrequest = FriendRequest(requester=self.request.user, receiver_id=user_id, **serializer.validated_data)
            friendrequest.save()
        print(request_exists)


class ListAcceptedFriends(ListAPIView):
    serializer_class = AcceptedFriends

    # lists all the friend requests
    def get_queryset(self):
        queryset = FriendRequest.objects.filter(Q(requester=self.request.user, status='accepted') | Q(receiver=self.request.user, status='accepted'))
        return queryset


# lists, updates and deletes friend requests
class GetUpdateDeleteFriendRequest(RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    lookup_url_kwarg = 'friendrequest_id'
    permission_classes = [IsAuthenticated, IsReceiverOfFriendRequestOrReadOnly]


# gets logged in user's profile and updates public information
class GetMyProfile(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfPostOrReadOnly]
    queryset = User.objects.all()

    def get_queryset(self):
        self.kwargs['pk'] = self.request.user.id
        return self.queryset

    def post(self, request):
        user = User.objects.filter(username=self.request.user)
        user.update(**request.data)
        return Response('Profile is updated')
