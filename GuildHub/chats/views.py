# chats/views.py
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.views import APIView

from users.mixins import user_is_not_banned
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


class CreateOrGetChat(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user1 = request.user
        user2_nickname = kwargs.get('nickname')  # Получаем nickname из kwargs

        try:
            user2 = User.objects.get(nickname=user2_nickname)  # Ищем пользователя по nickname
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

        if user1 == user2:
            return Response({'detail': 'You cannot create a chat with yourself.'}, status=400)

        # Найти существующий чат с этими участниками
        chat = Chat.objects.filter(participants=user1).filter(participants=user2).distinct().first()

        if chat is None:
            # Создать новый чат, если он не существует
            chat = Chat.objects.create()
            chat.participants.set([user1, user2])
            created = True
        else:
            created = False

        return Response({'chat_id': chat.id, 'created': created})


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(nickname=request.user.nickname)
        user_data = [{"id": user.id, "nickname": user.nickname} for user in queryset]
        return Response(user_data, status=status.HTTP_200_OK)


@login_required
def select_user(request):
    return render(request, 'chats/select_user.html')


@login_required
@user_is_not_banned
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all()  # Assuming you have a related name 'messages'
    return render(request, 'chats/chat_room.html', {
        'chat': chat,
        'messages': messages,
    })


@login_required
@user_is_not_banned
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chats/chat_list.html', {'chats': chats})

@csrf_exempt
def chat_messages(request, chat_id):
    if request.method == 'GET':
        messages = Message.objects.filter(chat_id=chat_id).values('sender__nickname', 'content', 'timestamp')
        return JsonResponse(list(messages), safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        user = request.user

        if content and user.is_authenticated:
            chat = Chat.objects.get(id=chat_id)
            message = Message.objects.create(chat=chat, sender=user, content=content)
            message.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failure'}, status=400)
