from django.contrib import admin

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient

# Register your models here.
@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'capital']

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name','province']

@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ['name','category']

@admin.register(Dish_Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ['dish','ingridient','quantity']