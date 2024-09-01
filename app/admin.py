from django.contrib import admin
from . models import *

admin.site.register(Temperature)
admin.site.register(Humidity)
admin.site.register(Stage)