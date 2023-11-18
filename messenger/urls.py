from django.urls import path
from messenger import views as view_messenger

urlpatterns = [
    path('chat/<int:task_id>/', view_messenger.view_chat, name='view_chat'),
    path('send_message/<int:task_id>/', view_messenger.send_message, name='send_message'),
]