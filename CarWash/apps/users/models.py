from django.db import models

# Create your models here.

class Single_User(models.Model):
    username = models.CharField("имя пользователя", max_length=50)
    password = models.CharField("пароль", max_length=100)


