from django.urls import path
from django.conf.urls import url


'''
URL привязки локальные
'''

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'), # доманяя страница
    path('register/', views.register, name='register'), # страница регистрации
    path('login/', views.login, name='login'),
    #path('video/', views.display_video, name="video"), # так пишет что видео нет
    url(r'^video/(?P<vid>\w+)/$',views.display_video), # а так он в display_video САМ ПЕРЕДАЕТ ВИДЕС
]
