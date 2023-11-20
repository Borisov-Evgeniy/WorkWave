from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileForm, AuthenticationForm
from .models import CustomUser

def main_page(request):
    return render(request, 'accounts/index.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Обработка данных профиля пользователя + фото
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            try:
                profile_form.save()
            except ValidationError as e:
                return HttpResponseServerError(f"Error while saving user profile: {e}")
    else:
        profile_form = UserProfileForm(instance=request.user)


    return render(request, 'accounts/profile.html', {'profile_form': profile_form})

def registration_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        registration_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if "login" in request.POST and login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')

        elif "register" in request.POST and registration_form.is_valid() and profile_form.is_valid():
            registration_form = CustomUserCreationForm(request.POST)
            profile_form = UserProfileForm(request.POST, request.FILES)

            if registration_form.is_valid() and profile_form.is_valid():
                try:
                    with transaction.atomic():
                        user = registration_form.save()
                        user.photo_user = profile_form.cleaned_data['photo_user']
                        user.save()
                        login(request, user)
                        return redirect('profile')
                except Exception as e:
                    return HttpResponseServerError(f"Error while saving user: {e}")
    else:
        login_form = AuthenticationForm()
        registration_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html', {'login_form': login_form, 'registration_form': registration_form, 'profile_form': profile_form})
