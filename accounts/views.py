from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser

def main_page(request):
    return render(request, 'accounts/index.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/register.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'accounts/register.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('profile')


# def logoutuser(request):
#     if request.method == 'POST':
#         # Выход пользователя при POST-запросе
#         logout(request)
#         return redirect('home')
#
#     # Редирект на home при GET-запросе
#     return redirect('home')

def logoutuser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='register', redirect_field_name='profile')
def profile_view(request):
    # получение данных пользователя и профиля для отображения на странице профиля
    user = request.user
    profile, created = CustomUser.objects.get_or_create(username=user.username)
    profile_form = UserProfileForm(instance=profile)  # создание экземпляра формы профиля

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()

    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile})

def registration_view(request):
    login_form = AuthenticationForm()  #login_form срабатывает всегда
    registration_form = CustomUserCreationForm()  #registration_form  срабатывает всегда
    profile_form = UserProfileForm()
    if request.method == 'POST':
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            try:
                with transaction.atomic():
                    user = registration_form.save()
                    print("User saved successfully:", user)  # Добавьте эту строку
                    login(request, user)
                    return redirect('profile')
            except Exception as e:
                print("Error while saving user:", e)  # Добавьте эту строку
        else:
            print("Invalid form data:", registration_form.errors)

            # if request.method == 'POST':
    #     if "login" in request.POST:
    #         login_form = AuthenticationForm(request, data=request.POST)
    #         if login_form.is_valid():
    #             username = login_form.cleaned_data.get('username')
    #             password = login_form.cleaned_data.get('password')
    #             user = authenticate(request, username=username, password=password)
    #             if user is not None:
    #                 login(request, user)
    #                 return redirect('profile')
    #
    #     elif "register" in request.POST:
    #         registration_form = CustomUserCreationForm(request.POST)
    #         profile_form = UserProfileForm(request.POST, request.FILES)
    #         if registration_form.is_valid() and profile_form.is_valid():
    #             print(registration_form.cleaned_data)
    #             user = registration_form.save()
    #             profile = profile_form.save(commit=False)
    #             profile.user = user
    #             profile.save()
    #             login(request, user)
    #             return redirect('profile')
    else:
        login_form = AuthenticationForm()
        registration_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html',
                  {'login_form': login_form, 'registration_form': registration_form, 'profile_form': profile_form})
