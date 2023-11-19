from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

@login_required
def view_chat(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # сообщения для данного задания
    messages = Message.objects.filter(task=task)

    context = {'task': task, 'messages': messages}
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