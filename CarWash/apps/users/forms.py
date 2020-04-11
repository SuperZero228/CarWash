# Здесь хранятся все формы

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Создание пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)


    # Конфигурации класса
    class Meta:
        model = User # в форме создается модель пользователя при form.save()
        fields = ['username', 'email', 'password1', 'password2']