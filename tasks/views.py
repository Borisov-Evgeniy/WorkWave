from django.shortcuts import render, redirect
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
    tasks_list = Task.objects.all().order_by('-created_at')

    paginator = Paginator(tasks_list, 12)  # 12 задач на странице
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)

@require_POST
def take_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        task.executor = request.user  # Предполагается, что пользователь авторизован
        task.save()
        return JsonResponse({'message': 'Задание успешно взято'})
    except Task.DoesNotExist:
        return JsonResponse({'message': 'Задание не найдено'}, status=404)