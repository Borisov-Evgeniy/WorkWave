from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserProfileForm

def main_page(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('register')  # Замените 'profile' на URL вашего профиля
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    # Здесь вы можете получать данные пользователя и профиля для отображения на странице профиля
    user = request.user
    profile = user.userprofile
    return render(request, 'profile.html', {'user': user, 'profile': profile})

def registration_view(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if registration_form.is_valid() and profile_form.is_valid():
            user = registration_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('register')  # Замените 'profile' на URL вашего профиля
    else:
        registration_form = RegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'accounts/register.html', {'registration_form': registration_form, 'profile_form': profile_form})
