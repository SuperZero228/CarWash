from django.db import models


# УСТАРЕВШИЕ МОДЕЛИ ДЛЯ SQLITE!

# Модель пользователя
class Single_User(models.Model):
    username = models.CharField("имя пользователя", max_length=50)
    password = models.CharField("пароль", max_length=100)

# Модель видео
class Video(models.Model):
    video_id = models.CharField(blank=False,max_length=500)
    file_name = models.CharField(blank=False, max_length=500)

    def __str__(self):
        return self.video_id