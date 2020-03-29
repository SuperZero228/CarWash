from django.urls import path


'''
URL привязки локальные
'''

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'), # доманяя страница
    path('register/', views.register, name='register'), # страница регистрации
    path('login/', views.login, name='login')
]