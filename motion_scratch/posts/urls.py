from django.urls import path

from posts.views import ToggleLike, ListCreatePosts, GetPostsOfUser, GetDeleteUpdatePostView, LikedByUser, \
    ListCreateComments, GetPostsOfFollowedUsers, GetPostsOfFriends

urlpatterns = [
    path('toggle-like/<int:post_id>/', ToggleLike.as_view()),
    path('', ListCreatePosts.as_view()),
    path('<int:post_id>/', GetDeleteUpdatePostView.as_view()),
    path('user/<int:owner_id>/', GetPostsOfUser.as_view()),
    path('following/', GetPostsOfFollowedUsers.as_view()),
    path('friends/', GetPostsOfFriends.as_view()),
    path('likes/', LikedByUser.as_view()),
    path('comments/<int:post_id>/', ListCreateComments.as_view()),

]
