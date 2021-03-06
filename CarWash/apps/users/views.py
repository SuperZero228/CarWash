from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
import os
import pyrebase
import cv2

# ОБЯЗАТЕЛЬНО СПЕРЕДИ ПИСАТЬ users !!!

from CarWash.apps.users.license_plate_detection import license_plate_recognition_v2
from CarWash.apps.users.parking_lot_detection import parking_lot_detection

parking_downloadToken = None # Эта переменная нужна именно глобально для получения URL обработанного фото - без нее БАГ
license_downloadToken = None
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

auth = firebase.auth() # регистраци и вход пользователей

db = firebase.database() # текстовые данные

storage = firebase.storage() # медиа-файлы



######################################################################################
# Это вьюшка для страницы регистрации.
def register(request):
    if request.method == 'POST': # Если был создан POST запрос на регистрацию, то форма создается со всеми данными запроса
        email = request.POST.get('email') # эти поля взяты из forms.py
        password = request.POST.get('password1')
        username = request.POST.get('username')

        # Создается пользователь и сохраняется в FireBase
        user = auth.create_user_with_email_and_password(email, password)

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

        return render(request, 'users/index.html', {"logged_in":logged_in})
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
    #video_url = "C:/Users/idrdi/OneDrive/Desktop/CarWash/media/1.mp4"

    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False
    return render(request, 'users/videos.html', {"logged_in": logged_in, "url":video_url})

# Функция сохраняет полученные в ходе работы данные в FireBase
def save_to_db(processed_parking, processed_license, text):

    # Если в put прописать напрямую processed_parking и processed_license, то он выдаст ошибку
    # Так что надо сначала эти фотки сохранить в папке а потом поместить их в FireBase и удалить из папки
    cv2.imwrite(settings.MEDIA_ROOT + r"\output\processed_parking.jpg", processed_parking)
    cv2.imwrite(settings.MEDIA_ROOT + r"\output\processed_license.jpg", processed_license)

    # Помещаем обработанное фото парковки в БД (Storage/users/email/images/...)
    parking_put_response = storage.child('/users').child(auth.current_user["localId"]).child("images/processed_parking.jpg").put(settings.MEDIA_ROOT + "output\processed_parking.jpg")
    license_put_response = storage.child('/users').child(auth.current_user["localId"]).child("images/processed_license.jpg").put(settings.MEDIA_ROOT + "output\processed_license.jpg")

    os.remove(settings.MEDIA_ROOT + r"\output\processed_parking.jpg")
    os.remove(settings.MEDIA_ROOT + r"\output\processed_license.jpg")

    print("PARKING_PUT_RESPONSE")
    for key, value in parking_put_response.items():
        print(key + " : " + value)

    # Глоабальная переменная для скачивание фото с парковкой
    global parking_downloadToken
    parking_downloadToken = parking_put_response['downloadTokens']
    # Глобальная переменная для скачивания фото с номерами
    global license_downloadToken
    license_downloadToken = license_put_response['downloadTokens']

    # Помещаем текст с номера в БД (Database/users/email/number_text...)
    db.child('/users').child(auth.current_user["localId"]).set(text)

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

        # Фотка обработанной парковки
        processed_parking = parking_lot_detection.process(parking_img, show_steps)

        # ДЕТЕКТ НОМЕРОВ
        # Вместо того, чтобы показываться во вспылвающем окне, обработанная фотография записывается в файл,
        # который потом будет загруже на HTML страницу
        print("\n\nПроизводится распознавание номеров автомобиля.")
        plate_img = cv2.imread(settings.MEDIA_ROOT + "input/bmw.jpg")

        # Текст с распознанного номера
        text, processed_license = license_plate_recognition_v2.process(plate_img, show_steps)

        save_to_db(processed_parking, processed_license, text)

        print("\n\nРабота завершена! Результаты можно видеть в папке media/output\n\n")
        print("\nРезультаты также были сохранены в FireBase")

        # перенаправление на страницу с результатами
        return redirect('../results')





# Функция показывает фотки, обработанные OpenCV
def show_results(request):
    if auth.current_user is not None:
        logged_in = True
    else:
        logged_in = False

    text_response = db.child('/users').child(auth.current_user['localId']).get()
    # Это текст с номера
    text = str(text_response.val())


    # Это ссылка на фотографию с распознанной парковкой
    # В аргументах get_url ОБЯЗАТЕЛЬНО надо указывать downloadToken - это фиксит баг разработчика PyreBase
    parking_image_url = storage.child('/users ').child(auth.current_user["localId"]).child("images/processed_parking.jpg").get_url(parking_downloadToken)
    license_image_url = storage.child('/users ').child(auth.current_user["localId"]).child("images/processed_license.jpg").get_url(license_downloadToken)

    # Необходимо удалить две цифры из URL фотографии, чтобы она кооректно отображалась
    if "/o/users%20" in parking_image_url:
        parking_image_url = parking_image_url.replace("/o/users%20", "/o/users")
    if "/o/users%20" in license_image_url:
        license_image_url = license_image_url.replace("/o/users%20", "/o/users")


    return render(request, 'users/show_results.html', {"logged_in": logged_in, "text": text, "parking_image_url": parking_image_url, "license_image_url":license_image_url})