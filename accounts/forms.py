from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            #               !!!                 #
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'templates/account/register.html', {'form': form})