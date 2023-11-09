from django.urls import path
from . import views

urlpatterns = [

    path('create_task/', views.create_task, name='create_task'),
    path('task_list/', views.open_create_task_modal, name='task_list'),

]
