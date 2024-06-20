from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)  # Сохраняем объект, чтобы получить pk
            participants = self.participants.all()
            if Chat.objects.filter(participants__in=participants).distinct().count() > 1:
                raise ValidationError('Chat with these participants already exists.')
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return ", ".join([user.nickname for user in self.participants.all()])


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'
