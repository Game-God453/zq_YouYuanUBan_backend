from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class ChatConnection(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connections_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="connections_user2", on_delete=models.CASCADE)
    last_message_user1 = models.BigIntegerField(default=0)
    last_message_user2 = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")  # 确保用户对是唯一的

    def __str__(self):
        return f"Connection between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    chat = models.ForeignKey(ChatConnection, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content}"