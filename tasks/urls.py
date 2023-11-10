from django.urls import path
from tasks import views as view_tasks

urlpatterns = [

    path('create_task/', view_tasks.create_task, name='create_task'),
    path('task_list/', view_tasks.task_list, name='task_list'),
    path('take_task/<int:task_id>/', view_tasks.take_task, name='take_task'),

]
