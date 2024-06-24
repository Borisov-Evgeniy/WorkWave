from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Task(models.Model):
    title = models.CharField(max_length=200)
    image_task = models.ImageField(upload_to='media/image_task/', null=True, blank=True)
    description = models.TextField()
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_tasks')
    executor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    canceled_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='canceled_tasks')
    canceled_at = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=255,null=True)
    def cancel_task(self, user):
        if not self.is_canceled:
            self.is_completed = False
            self.canceled_by = user
            self.canceled_at = timezone.now()
            self.executor = None
            try:
                self.save()
                print(f"Task {self.id} successfully canceled.")
            except Exception as e:
                print(f"Error saving canceled status for task {self.id}: {e}")
        else:
            print(f"Task {self.id} is already canceled.")

    @property
    def is_canceled(self):
        return bool(self.canceled_at)

    def __str__(self):
        return self.title
