from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

'''
URL привязки локальные
'''

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'), # доманяя страница
    path('register/', views.register, name='register'), # страница регистрации
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),  # базовая форма логина. template_name указывает на то, какую html сраницу надо загрузить
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    url(r'^video/(?P<vid>\w+)/$',views.display_video, name="video"), # а так он в display_video САМ ПЕРЕДАЕТ ВИДЕО
]
