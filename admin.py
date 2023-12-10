from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((Profile ,Message,Post ,Comment ,Categorise))
# admin.site.register(Message)