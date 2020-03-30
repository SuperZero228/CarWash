from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)