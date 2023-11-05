from django.db import models
from accounts.models import CustomUser

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_tasks')
    executor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
