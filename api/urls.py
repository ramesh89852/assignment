from django.urls import path
from .views import (UserSearchView, send_friend_request, accept_friend_request,
                    reject_friend_request, FriendListView, PendingRequestsView,
                    UserSignupView,UserLoginView)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/<int:user_id>/', send_friend_request, name='send-friend-request'),
    path('friend-request/accept/<int:request_id>/', accept_friend_request, name='accept-friend-request'),
    path('friend-request/reject/<int:request_id>/', reject_friend_request, name='reject-friend-request'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('friend-requests/pending/', PendingRequestsView.as_view(), name='pending-requests'),
]
