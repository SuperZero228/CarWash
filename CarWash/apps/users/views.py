from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse


# Это вьюшка для страницы регистрации.
def register(request):
    if request.method == 'POST': # Если был создан POST запрос на регистрацию, то форма создается со всеми данными запроса
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # СОХРАНЕНИЕ ПОЛЬЗОВАТЕЛЯ
            form.save()

            username = form.cleaned_data.get('username')
            # Бывают такие flash-сообщения
            # messages.debug
            # messages.info
            # messages.success
            # messages.warning
            # messages.error
            messages.success(request, f'Аккаунт создан, {username}')
            # ЗДЕСЬ НАДО РЕНДЕРИТЬ СТРАНИЦУ С ВИДЕО!
            return render(request, 'users/index.html', {"form": form})
        else:
            print("Form is not valid!")
    else:
        form = UserCreationForm() # Если нет, то создается просто пустая форма
        print(1)
    return render(request, 'users/register.html', {'form': form})

# Домашняя страница
def index(request):
    return render(request, 'users/index.html')

# Станица входа
def login(request):
    return render(request, 'users/login.html')

