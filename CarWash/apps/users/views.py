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

        # На почту отправляется письмо для подтверждения почты
        auth.send_email_verification(user["idToken"])
        messages.info(request, f'На Вашу почту было отправлено письмо для подтверждения регистрации')
        return redirect('../login')

    return render(request, 'users/register.html')

# Домашняя страница
def index(request):
    return render(request, 'users/index.html')

# Станица входа
def login(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        login = auth.sign_in_with_email_and_password(email, password)

        #messages.info(request, f'Вы успешно вошли в аккаунт!')
        video_url = find_video()
        return render(request, 'users/videos.html', {"logged_in": True, "url":video_url})
    else:
        return render(request, 'users/login.html')

def logout(request):
    auth.current_user = None # так делается выход из аккаунта
    return render(request, 'users/logout.html')

# Функция получает путь к файлу с видео
def find_video():


    video_name = ""
    for fname in os.listdir(settings.MEDIA_ROOT):
        if ".mp4" in fname:
            video_name = fname
            break
    """
    video_name = "1.mp4" # надо сделать, чтобы искал любой видос !!! БАГ
    """

    video_url = settings.MEDIA_ROOT + video_name

    return video_url
