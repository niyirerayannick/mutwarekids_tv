from django.contrib import admin
from .models import Profile, CustomUser
from kidtv.models import Video 

admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Video)
