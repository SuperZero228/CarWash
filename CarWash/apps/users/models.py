from django.db import models


# Модель пользователя
class Single_User(models.Model):
    username = models.CharField("имя пользователя", max_length=50)
    password = models.CharField("пароль", max_length=100)

# Модель видео
class Video(models.Model):
    name = models.FileField(max_length=500)
    videofile = models.FileField(upload_to="videos/", null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)

    