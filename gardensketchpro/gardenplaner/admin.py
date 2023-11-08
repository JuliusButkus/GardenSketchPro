from django.contrib import admin
from . import models


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_lt', 'description_en', 'description_lt')
    list_filter = ('name_en', 'name_lt')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_lt', 'description_en', 'description_lt')
    list_filter = ('name_en', 'name_lt')


class PlantTimeAdmin(admin.ModelAdmin):
    list_display = ('month_en', 'month_lt', 'first_day', 'last_day')
    list_filter = ('month_en', 'month_lt')


class PlantAdmin(admin.ModelAdmin):
    list_display = (
        'name_en', 'name_lt', 'description_en', 'description_lt',
        'type', 'planting_time'
        )
    list_filter = ('name_en', 'name_lt', 'type')



admin.site.register(models.Type, TypeAdmin)
admin.site.register(models.Color, ColorAdmin)
admin.site.register(models.PlantTime, PlantTimeAdmin)
admin.site.register(models.Plant, PlantAdmin)
