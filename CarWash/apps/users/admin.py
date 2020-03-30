from django.contrib import admin


from users.models import Single_User
from users.models import Video

# Register your models here.
admin.site.register(Single_User)
admin.site.register(Video)
