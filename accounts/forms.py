from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[('customer', 'Заказчик'), ('executor', 'Исполнитель')], widget=forms.Select)

class CustomRegistrationForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

class RegistrationForm(CustomRegistrationForm):
    description = forms.CharField(widget=forms.Textarea)
    photo_user = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role', 'description', 'photo_user')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo_user', 'name', 'description')

def register(request):
    if request.method == 'POST':
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            return redirect('home')
    else:
        registration_form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'registration_form': registration_form})
