from django.urls import path
from accounts import views as accounts_views

urlpatterns = [
    path('login/', accounts_views.login_view, name='login'),
    path('profile/', accounts_views.profile_view, name='profile'),
    path('register/', accounts_views.registration_view, name='register'),
]
