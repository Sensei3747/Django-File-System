from django.db import models
from file.models import UserProfile

class ChatTable(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_chats', db_column='sender_id')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_chats', db_column='receiver_id')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f' {self.sender.username} to {self.receiver.username} at {self.timestamp}'
    

