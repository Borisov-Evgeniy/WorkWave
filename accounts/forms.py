from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[('customer', 'Заказчик'), ('executor', 'Исполнитель')], widget=forms.Select)
    description = forms.CharField(widget=forms.Textarea)
    photo_user = forms.ImageField(required=False, widget=forms.ClearableFileInput())

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'photo_user', 'name', 'description')

class UserProfileForm(forms.ModelForm):
    photo_user = forms.FileField(label='Фото профиля', required=False)
    class Meta:
        model = CustomUser
        fields = ('photo_user', 'name', 'description', 'role')

def register(request):
    if request.method == 'POST':
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            return redirect('profile')
    else:
        registration_form = RegistrationForm()

    return render(request, 'accounts/register.html', {'registration_form': registration_form})