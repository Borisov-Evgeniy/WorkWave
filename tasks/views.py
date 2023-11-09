from django.shortcuts import render, redirect
from .forms import CreateTask

@login_required
def create_task(request):
    if request.method == 'POST':
        create_task_form = CreateTask(request.POST, request.FILES)
        if create_task_form.is_valid():
            try:
                task = create_task_form.save(commit=False)
                task.user = request.user  # привязка задания к текущему пользователю
                task.save()
                return redirect('home')
            except Exception as e:
                return HttpResponseServerError(f"Error while saving user: {e}")
    else:
        create_task_form = CreateTask()

    return render(request, 'accounts/index.html', {'create_task_form': create_task_form})

