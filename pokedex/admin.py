from django.contrib import admin
from .models import Pokemon, Entrenador, Gym, Backup


# Register your models here.

admin.site.register(Pokemon)
admin.site.register(Entrenador)
admin.site.register(Gym)
admin.site.register(Backup)