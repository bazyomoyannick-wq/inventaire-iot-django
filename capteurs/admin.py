from django.contrib import admin

from .models import Capteur


@admin.register(Capteur)
class CapteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_capteur", "emplacement", "actif")
    list_filter = ("type_capteur", "actif")
    search_fields = ("nom", "emplacement")
