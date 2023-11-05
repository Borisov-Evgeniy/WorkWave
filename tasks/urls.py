from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]