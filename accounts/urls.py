from django.urls import path
from accounts import views as accounts_views

urlpatterns = [
    path('profile/', accounts_views.profile_view, name='profile'),
    path('register/', accounts_views.registration_view, name='register'),
    path('login/', accounts_views.registration_view, name='login'),
    path('', accounts_views.main_page, name='home'),
    path('logout/', accounts_views.logoutuser, name='logout'),
]
