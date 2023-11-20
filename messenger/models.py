from django.db import models
from accounts.models import CustomUser
from tasks.models import Task

class Message(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.content}"