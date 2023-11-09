from django import forms
from .models import Task

class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'image_task','due_date')