from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
import os
import fnmatch

# ОБЯЗАТЕЛЬНО СПЕРЕДИ ПИСАТЬ users !!!
from users.models import Single_User
from users.models import Video
from users.forms import UserRegisterForm # кастомная форма регистрации

# Это вьюшка для страницы регистрации.
def register(request):
    if request.method == 'POST': # Если был создан POST запрос на регистрацию, то форма создается со всеми данными запроса
        form = UserRegisterForm(request.POST)
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
            messages.success(request, f'Аккаунт создан!')
            return redirect('../login')
        else:
            print("Form is not valid!")
    else:
        form = UserRegisterForm() # Если нет, то создается просто пустая форма
        print(1)
    return render(request, 'users/register.html', {'form': form})

# Домашняя страница
def index(request):
    return render(request, 'users/index.html')

# Станица входа
def login(request):
    return render(request, 'users/login.html')

# Страница с видео
def display_video(request,vid=None):
    if vid is None:
        return HttpResponse("No video!")

    # Здесь идет поиск видео с разными расширениями. У меня они mp4. Так что закоменчу
    """
    video_name = ""
    for fname in os.listdir(settings.MEDIA_ROOT):
        if fnmatch.fnmatch(fname, vid+".*"): #using pattern to find the video file with given id and any extension
            video_name = fname
            break
    """

    video_name = vid+".mp4"

    # ..../media/1.mp4
    #video_url = settings.MEDIA_URL+video_name
    video_url = settings.MEDIA_ROOT + video_name

    return render(request, "users/videos.html", {"url":video_url})
