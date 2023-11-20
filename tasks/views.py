from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateTask
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Task
from django.http import JsonResponse

@login_required
def create_task(request):
    if request.method == 'POST':
        create_task_form = CreateTask(request.POST, request.FILES)
        if create_task_form.is_valid():
            try:
                task = create_task_form.save(commit=False)
                task.user = request.user  # привязка задания к текущему пользователю
                task.customer = request.user  # установка заказчика
                task.save()
                return redirect('home')
            except Exception as e:
                return HttpResponseServerError(f"Error while saving task: {e}")
    else:
        create_task_form = CreateTask()

    return render(request, 'tasks/create_task.html', {'create_task_form': create_task_form})

def task_list(request):
    query = request.GET.get('q')
    tasks_list = Task.objects.all().order_by('-created_at')

    if query:
        # фильтрация задач по заголовку
        tasks_list = tasks_list.filter(title__icontains=query)

    paginator = Paginator(tasks_list, 12)  # 12 задач на странице
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)

@require_POST
def take_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)

        # Проверяем, может ли текущий пользователь взять задание
        if can_take_task(request.user, task):
            task.executor = request.user
            task.canceled_at = None
            task.canceled_by = None
            task.save()
            return JsonResponse({'message': 'Задание успешно взято'})
        else:
            return JsonResponse({'error': 'Нельзя взять свое собственное задание или уже взято другим исполнителем.'}, status=400)

    except Task.DoesNotExist:
        return JsonResponse({'error': 'Задание не найдено'}, status=404)

def can_take_task(user, task):
    # функция проверки, может ли пользователь взять задание
    return user != task.customer and task.executor is None

def executor_tasks(request):
    # задания взятые текущим исполнителем
    executor_tasks = Task.objects.filter(executor=request.user)
    return render(request, 'tasks/executor_tasks.html', {'executor_tasks': executor_tasks})

def customer_tasks(request):
    # задания созданные текущим заказчиком
    customer_tasks = Task.objects.filter(customer=request.user)
    return render(request, 'tasks/customer_tasks.html', {'customer_tasks': customer_tasks})

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user == task.customer:
        task.delete()
        return JsonResponse({'message': 'Задание успешно удалено'})
    else:
        return JsonResponse({'message': 'У вас нет разрешения на удаление этой задачи'}, status=403)

def cancel_tasks(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        try:
            task.cancel_task(request.user)
            print(f"Task {task_id} successfully canceled by user {request.user.username}")
        except Exception as e:
            print(f"Error canceling task {task_id}: {e}")
        return redirect('executor_tasks')

    return render(request, 'tasks/executor_tasks.html', {'task': task})