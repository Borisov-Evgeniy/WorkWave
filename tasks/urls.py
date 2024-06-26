from django.urls import path
from tasks import views as view_tasks
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('create_task/', view_tasks.create_task, name='create_task'),
    path('task_list/', view_tasks.task_list, name='task_list'),
    path('take_task/<int:task_id>/', view_tasks.take_task, name='take_task'),
    path('executor_tasks/', view_tasks.executor_tasks, name='executor_tasks'),
    path('customer_tasks/', view_tasks.customer_tasks, name='customer_tasks'),
    path('delete_task/<int:task_id>/', view_tasks.delete_task, name='delete_task'),
    path('cancel_task/<int:task_id>/', view_tasks.cancel_tasks, name='cancel_task'),
    path('map/', view_tasks.tasks_map_view, name='tasks_map'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)