from django.urls import path

from .views import ChatListCreate, MessageListCreate, CreateOrGetChat, select_user, chat_room, UserList, chat_list, \
    chat_messages

urlpatterns = [
    path('api/users/', UserList.as_view(), name='user-list'),
    path('select-user/', select_user, name='select-user'),
    path('chat/<int:chat_id>/', chat_room, name='chat-room'),
    path('chat-list/', chat_list, name='chat-list'),
    # API routes
    path('api/chats/', ChatListCreate.as_view(), name='chat-list-create'),
    path('api/chats/<int:chat_id>/messages/', chat_messages, name='chat-messages'),
    path('api/chats/create-or-get/', CreateOrGetChat.as_view(), name='create-or-get-chat'),
]
