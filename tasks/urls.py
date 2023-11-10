from django.urls import path
from tasks import views as view_tasks

urlpatterns = [

    path('create_task/', view_tasks.create_task, name='create_task'),
    path('task_list/', view_tasks.task_list, name='task_list'),
    path('take_task/<int:task_id>/', view_tasks.take_task, name='take_task'),
    path('executor_tasks/', view_tasks.executor_tasks, name='executor_tasks'),
    path('customer_tasks/', view_tasks.customer_tasks, name='customer_tasks'),
    path('delete_task/<int:task_id>/', view_tasks.delete_task, name='delete_task'),

]
