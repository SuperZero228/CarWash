from django.urls import path
from django.conf.urls import url


'''
URL привязки локальные
'''

from . import views


app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),  # доманяя страница
    path('register/', views.register, name='register'),  # страница регистрации
    path('login/', views.login, name='login'),  # базовая форма логина. template_name указывает на то, какую html сраницу надо загрузить
    path('logout/', views.logout, name='logout'),
    path('opencv/', views.activate_opencv, name="test"),  # пробую тестить OpenCV
    path('video/', views.display_video, name="video"),  # на этой странице показывается видео, но только если пользователь вошел в аккаунт
    path('results/', views.show_results, name='results'), # показывает все фотки, обработанные OpenCV
]
