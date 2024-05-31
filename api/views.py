from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .models import User
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer,UserSignupSerializer, UserLoginSerializer
from datetime import datetime, timedelta

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(
            Q(email__iexact=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, user_id):
    if request.user.id == user_id:
        return Response({'error': 'You cannot send a friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(from_user=request.user, to_user_id=user_id).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    now = datetime.now()
    one_minute_ago = now - timedelta(minutes=1)
    recent_requests = FriendRequest.objects.filter(from_user=request.user, timestamp__gte=one_minute_ago).count()

    if recent_requests >= 3:
        return Response({'error': 'You can not send more than 3 friend requests within a minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    to_user = User.objects.get(id=user_id)
    friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_400_BAD_REQUEST)
    friend_request.accepted = True
    friend_request.save()
    return Response(FriendRequestSerializer(friend_request).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found'}, status=status.HTTP_400_BAD_REQUEST)
    friend_request.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__accepted=True) |
            Q(received_requests__from_user=self.request.user, received_requests__accepted=True)
        ).distinct()

class PendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=False)
