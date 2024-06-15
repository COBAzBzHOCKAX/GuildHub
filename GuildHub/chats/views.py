# chats/views.py
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from users.models import User  # Correct import for the custom User model
from rest_framework.permissions import IsAuthenticated

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status

class ChatListCreate(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chats.all()

    def perform_create(self, serializer):
        chat = serializer.save()
        chat.participants.add(self.request.user)

class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat__id=chat_id)

    def perform_create(self, serializer):
        chat = Chat.objects.get(id=self.kwargs['chat_id'])
        serializer.save(sender=self.request.user, chat=chat)

class CreateOrGetChat(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user1 = request.user
        user2_username = request.data.get('username')
        try:
            user2 = User.objects.get(username=user2_username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        chats = Chat.objects.filter(participants=user1).filter(participants=user2)
        if chats.exists():
            chat = chats.first()
            return Response(ChatSerializer(chat).data)
        else:
            chat = Chat.objects.create()
            chat.participants.add(user1, user2)
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(username=request.user.username)
        user_data = [{"id": user.id, "username": user.username} for user in queryset]
        return Response(user_data, status=status.HTTP_200_OK)

def select_user(request):
    return render(request, 'select_user.html')

def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, 'chat_room.html', {'chat_id': chat.id})
