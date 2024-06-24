from django import forms
from .models import Task

class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'image_task','due_date','address')
        labels = {
            'title': 'Задача',
            'description': 'Описание',
            'image_task': 'Фото',
            'due_date': 'Дата выполнения',
            'address': 'Адрес задания'
        }