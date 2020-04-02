from django.urls import path
from django.conf.urls import url


'''
URL привязки локальные
'''

from . import views

app_name = 'users'
urlpatterns = [
    path('index/', views.index, name='index'), # доманяя страница
    path('register/', views.register, name='register'), # страница регистрации
    path('login/', views.login, name='login'),  # базовая форма логина. template_name указывает на то, какую html сраницу надо загрузить
    path('logout/', views.logout, name='logout'),

]
