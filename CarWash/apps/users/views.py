from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
import os
<<<<<<< Updated upstream
import pyrebase
import cv2
||||||| merged common ancestors
import fnmatch
=======
import fnmatch
import pyrebase
>>>>>>> Stashed changes

# ОБЯЗАТЕЛЬНО СПЕРЕДИ ПИСАТЬ users !!!

<<<<<<< Updated upstream
from CarWash.apps.users.license_plate_detection import license_plate_recognition_v2
from CarWash.apps.users.parking_lot_detection import parking_lot_detection

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

database = firebase.database()





######################################################################################
||||||| merged common ancestors
=======

############################################
# Конфиг для БД FireBase
config = {
    'apiKey': "AIzaSyBnsFHlZ9IP7kATKMILibYxT4y2_CRWUrM",
    'authDomain': "carwash-838f3.firebaseapp.com",
    'databaseURL': "https://carwash-838f3.firebaseio.com",
    'projectId': "carwash-838f3",
    'storageBucket': "carwash-838f3.appspot.com",
    'messagingSenderId': "548753653087",
    'appId': "1:548753653087:web:1dcba0736eff005002caea",
    'measurementId': "G-7YLLEJ4SX7"
  };

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

#############################################

>>>>>>> Stashed changes
# Это вьюшка для страницы регистрации.
def register(request):
    if request.method == 'POST': # Если был создан POST запрос на регистрацию, то форма создается со всеми данными запроса
<<<<<<< Updated upstream
        email = request.POST.get('email') # эти поля взяты из forms.py
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
||||||| merged common ancestors
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
=======

        # Создается форма, которую пользователь заполняет, и затем из нее мы получаем данные
        form = UserRegisterForm(request.POST)

        # Это сохранение в FireBase (более поздняя фича)
        email = request.POST.get('email')
        password = request.POST.get('password1')  # эти поля берутся из forms.py fields


        # Если все удачно, то перенаправляется на страницу входа
        if form.is_valid():
            # В FireBase создается пользователь
            user = auth.create_user_with_email_and_password(email, password)
            # Подтверждение почты
            auth.send_email_verification(user["idToken"])
            messages.success(request, f'Аккаунт создан!')
            form =
            return redirect('../login')
    else:
        form = UserRegisterForm() # Если нет, то создается просто пустая форма

    # КОГДА ВЫЗЫВАЕТСЯ ФУНКЦИЯ register, то вот это выводится на ЭКРАН
    return render(request, 'users/register.html', {'form': form})
>>>>>>> Stashed changes

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

        return render(request, 'users/index.html', {"logged_in":logged_in})
        #return display_video(request)


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
    for fname in os.listdir(settings.MEDIA_ROOT + "input/"):
        if ".mp4" in fname:
            video_name = fname
            break
    """
    video_name = "1.mp4" # надо сделать, чтобы искал любой видос !!! БАГ
    """

    video_url = settings.MEDIA_ROOT + "input/" + video_name
    print("VIDEO PATH ", video_url)

    return video_url


# Функция рендерит страницу, на которой воспроизводится видео

def display_video(request):

    video_url = find_video()  # находится путь к видео в папке /media/

    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'users/videos.html', {"logged_in": logged_in, "url":video_url})


# Функция активирует работу OpenCV
# Также вызывает другие функции, связанные с OpenCV
def activate_opencv(request):
    # Сначала рендериться форма, где пользователь указывает, хочет ли он видеть этапы работы
    if request.method == "GET":
        return render(request, 'users/steps_form.html')
    # У самой форму метод POST, так что после ее заполнения выполнится это условие
    elif request.method == "POST":

        choice = request.POST.get("select")
        if choice == "yes":
            show_steps = True # переключается в зависимости от выбора пользователя
        elif choice == "no":
            show_steps = False

        # ДЕТЕКТ ПАРКОВОК
        # Вместо того, чтобы показываться во вспылвающем окне, обработанная фотография записывается в файл,
        # который потом будет загруже на HTML страницу
        print("\n\nПроизводится распознавание парковочных зон.")
        parking_img = cv2.imread(settings.MEDIA_ROOT + 'input/empty.jpg')

        parking_lot_detection.process(parking_img, show_steps)

        # ДЕТЕКТ НОМЕРОВ
        # Вместо того, чтобы показываться во вспылвающем окне, обработанная фотография записывается в файл,
        # который потом будет загруже на HTML страницу
        print("\n\nПроизводится распознавание номеров автомобиля.")
        plate_img = cv2.imread(settings.MEDIA_ROOT + "input/bmw.jpg")
        text = license_plate_recognition_v2.process(plate_img, show_steps)

        print("\n\nРабота завершена! Результаты можно видеть в папке media/output\n\n")

        # перенаправление на страницу с результатами
        return redirect('../results')





# Функция показывает фотки, обработанные OpenCV
def show_results(request):
    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False

    return render(request, 'users/show_results.html', {"logged_in": logged_in})
