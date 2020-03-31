from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
import os
import fnmatch
import pyrebase

# ОБЯЗАТЕЛЬНО СПЕРЕДИ ПИСАТЬ users !!!
from users.models import Single_User
from users.models import Video
from users.forms import UserRegisterForm # кастомная форма регистрации



#######################################################################################
# конфиг для FireBase
config = {
    'apiKey': "AIzaSyBnsFHlZ9IP7kATKMILibYxT4y2_CRWUrM",
    'authDomain': "carwash-838f3.firebaseapp.com",
    'databaseURL': "https://carwash-838f3.firebaseio.com",
    'projectId': "carwash-838f3",
    'storageBucket': "carwash-838f3.appspot.com",
    'messagingSenderId': "548753653087",
    'appId': "1:548753653087:web:1dcba0736eff005002caea",
    'measurementId': "G-7YLLEJ4SX7"
  }

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
######################################################################################
# Это вьюшка для страницы регистрации.
def register(request):
    if request.method == 'POST': # Если был создан POST запрос на регистрацию, то форма создается со всеми данными запроса
        email = request.POST.get('email') # эти поля взяты из forms.py
        print("\n\n\n email is " + email + '\n\n\n')
        password = request.POST.get('password1')

        # Создается пользователь и сохраняется в FireBase
        user = auth.create_user_with_email_and_password(email, password)

        messages.success(request, f'Аккаунт создан!')
        return redirect('../login')
    else:
        print("Form is not valid!")
   
    return render(request, 'users/register.html')

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
