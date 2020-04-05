from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
import os
import fnmatch
import pyrebase
import cv2
import imutils

# ОБЯЗАТЕЛЬНО СПЕРЕДИ ПИСАТЬ users !!!
from users.models import Single_User
from users.models import Video
from users.forms import UserRegisterForm # кастомная форма регистрации

from . import parking_lot_detection



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
        username = request.POST.get('username')

        # Создается пользователь и сохраняется в FireBase
        user = auth.create_user_with_email_and_password(email, password)
        user["displayName"] = username

        # На почту отправляется письмо для подтверждения почты
        auth.send_email_verification(user["idToken"])
        messages.info(request, f'На Вашу почту было отправлено письмо для подтверждения регистрации')
        return redirect('../login')

    return render(request, 'users/register.html')

# Домашняя страница
def index(request):
    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'users/index.html', {"logged_in": logged_in})

# Станица входа
def login(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            login = auth.sign_in_with_email_and_password(email, password)
        except Exception:
            raise Exception

        if auth.current_user:
            logged_in = True
        else:
            logged_in = False

        return display_video(request)


        #return redirect("../video", {"logged_in": logged_in})
        # Это убираю, потому что теперь более сложная схема - с редиректом
        #return render(request, 'users/videos.html', {"logged_in": True, "url":video_url})
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


# Функция рендерит страницу, на которой воспроизводится видео

def display_video(request):

    video_url = find_video()  # находится путь к видео в папке /media/

    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'users/videos.html', {"logged_in": logged_in, "url":video_url})

# Функция вызывается другой функцией и реализует функионал OpenCV
def process_img():
    img = cv2.imread(r"C:\CREESTL\Programming\PythonCoding\semestr_3\parking_lot_detection\parking_lots\000002.jpg")
    img = imutils.resize(img, 400, 400)
    # Показ окна виснет и крашится
    #cv2.imshow("image", img)
    (H, W) = img.shape[:2]
    print("\nThe size of the image is: ", H, W, "\n")



# Надо в конце рендерить страницу videos.html и в словаре передать туда результат работы opencv
# а потом его надо будет через {{  }} вывести наверно
def activate_opencv(request):
    process_img()

    # В консоль надо смотреть когда это запускаю! Он там ждет ответа y/n
    img = cv2.imread(r'C:\CREESTL\Programming\PythonCoding\semestr_3\parking_lot_detection\parking_lots\empty.jpg')
    parking_lot_detection.process(img)



    return render(request, "users/index.html")



