from django.db import models

# Create your models here.
class Province(models.Model):
    name = models.TextField("Название")
    capital = models.TextField("Столица")
    population = models.TextField("Население")
    area = models.TextField("Площадь")

    class Meta:
        verbose_name = "Провинция"
        verbose_name_plural = "Провинции"

    def __str__(self) -> str:
        return self.name

class Ingridient(models.Model):
    name = models.TextField("Название")
    category = models.TextField("Категория")

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self) -> str:
        return self.name
    
class Dish(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    category = models.TextField("Категория")
    spice_level = models.TextField("Уровень остроты")
    province = models.ForeignKey("Province", on_delete=models.CASCADE, null=True, verbose_name = "Провинция")
    #ingridients = models.ManyToManyField(Ingridient, through="Dish_Ingridient")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self) -> str:
        return self.name

class Dish_Ingridient(models.Model):
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, null=True, verbose_name = "Блюдо")
    ingridient =  models.ForeignKey("Ingridient", on_delete=models.CASCADE, null=True, verbose_name = "Ингридиент")
    quantity = models.TextField("Количество")

    class Meta:
        verbose_name = "Блюдо_Ингридент"
        verbose_name_plural = "Блюда_Ингриденты"

