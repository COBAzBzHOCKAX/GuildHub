from django.urls import path

from .views import ChatListCreate, MessageListCreate, CreateOrGetChat, select_user, chat_room, UserList

urlpatterns = [
    path('api/users/', UserList.as_view(), name='user-list'),
    path('select-user/', select_user, name='select-user'),
    path('chat/<int:chat_id>/', chat_room, name='chat-room'),
    # API routes
    path('api/chats/', ChatListCreate.as_view(), name='chat-list-create'),
    path('api/chats/<int:chat_id>/messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('api/chats/create-or-get/', CreateOrGetChat.as_view(), name='create-or-get-chat'),
]
