from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from tasks.models import Task
from accounts import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

@login_required
def view_chat(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    messages = Message.objects.filter(task=task)

    sender = request.user
    receiver = task.customer if sender != task.customer else task.executor

    context = {
        'task': task,
        'messages': messages,
        'sender': sender,
        'receiver': receiver,
        'sender.photo.url': sender.photo_user,
        'sender.username': sender.username,
        'receiver.photo.url': receiver.photo_user,
        'receiver.username': receiver.username,
    }

    return render(request, 'messenger/chat.html', context)

@login_required
def send_message(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        content = request.POST.get('content', '')
        sender = request.user

        # проверка наличия исполнителя
        if task.executor:
            recipient = task.executor
        else:
            # если исполнителя нет
            recipient = task.customer

        message = Message.objects.create(
            task=task,
            sender=sender,
            recipient=recipient,
            content=content
        )

        return redirect('view_chat', task_id=task_id)

    return render(request, 'messenger/chat.html', {'task': task})