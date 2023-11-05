import workwave.settings
from django.urls import path
from django.conf import settings
from django.urls import path
from accounts import views as accounts_views
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', accounts_views.profile_view, name='profile'),
    path('register/', accounts_views.registration_view, name='register'),
    path('login/', accounts_views.registration_view, name='login'),
    path('', accounts_views.main_page, name='home'),
    path('logout/', accounts_views.logoutuser, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)