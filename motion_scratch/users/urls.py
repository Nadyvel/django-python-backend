from django.urls import path

from users.views import ToggleFollow, GetListOfUsers, CreateFriendRequest, ListAcceptedFriends, \
    AllLoggedInUserFollowers, PeopleLoggedInUserFollows, GetSpecificUserById, \
    GetUpdateDeleteFriendRequest, GetMyProfile

urlpatterns = [
    path('followers/toggle-follow/<int:user_id>/', ToggleFollow.as_view()),
    path('', GetListOfUsers.as_view()),
    path('<int:user_id>/', GetSpecificUserById.as_view()),
    path('friends/request/<int:user_id>/', CreateFriendRequest.as_view()),
    #path('friends/requests/<int:user_id>/', ListAcceptedFriends.as_view()),
    path('friends/requests/<int:friendrequest_id>/', GetUpdateDeleteFriendRequest.as_view()),
    path('friends/', ListAcceptedFriends.as_view()),
    path('followers/followers/', AllLoggedInUserFollowers.as_view()),
    path('followers/following/', PeopleLoggedInUserFollows.as_view()),
    path('me/', GetMyProfile.as_view()),

]

