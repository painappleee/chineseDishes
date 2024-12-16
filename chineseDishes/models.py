from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Province(models.Model):
    name = models.TextField("Название")
    capital = models.TextField("Столица")
    population = models.PositiveIntegerField("Население(чел.)")
    area = models.PositiveIntegerField("Площадь(кв.км.)")
    picture = models.ImageField("Изображение", null = True, upload_to= "chineseDishes" )


    class Meta:
        verbose_name = "Провинция"
        verbose_name_plural = "Провинции"

    def __str__(self) -> str:
        return self.name

class Ingridient(models.Model):

    class IngridientCategory(models.TextChoices):
        MEAT = 'Мясо','Мясо'
        MILK = 'Молочные продукты','Молочные продукты'
        SEREALS = 'Крупы','Крупы'


    category = models.CharField(
        max_length= 30,
        choices= IngridientCategory.choices,
        verbose_name="Категория")
    name = models.TextField("Название")


    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self) -> str:
        return self.name
    
class Dish(models.Model):

    class DishCategory(models.TextChoices):
        DESSERT = 'Десерт','Десерт'
        HOT = 'Горячее','Горячее'
        DRINK = 'Напиток','Напиток'

    name = models.TextField("Название")
    description = models.TextField("Описание")
    category = models.CharField(
        max_length= 30,
        choices= DishCategory.choices,
        verbose_name="Категория")
    spice_level = models.PositiveIntegerField(verbose_name="Уровень остроты", validators=[MaxValueValidator(10)])
    province = models.ForeignKey("Province", on_delete=models.CASCADE, null=True, verbose_name = "Провинция")
    picture = models.ImageField("Изображение", null = True, upload_to= "chineseDishes" )
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    #ingridients = models.ManyToManyField(Ingridient, through="Dish_Ingridient")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self) -> str:
        return self.name

class Dish_Ingridient(models.Model):
    class QuantityType(models.TextChoices):
        GR = 'гр','гр'
        ML = 'мл','мл'
        GLASS = ' ст.','ст.'
        SMLSPOON = 'ч.л.','ч.л.'
        BGSPOON = 'ст.л.','ст.л.'

    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, null=True, verbose_name = "Блюдо")
    ingridient =  models.ForeignKey("Ingridient", on_delete=models.CASCADE, null=True, verbose_name = "Ингридиент")
    quantity = models.PositiveIntegerField("Количество")
    typeQuantity = models.CharField(
        max_length= 10,
        choices= QuantityType.choices,
        verbose_name="Измерение")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Блюдо_Ингридент"
        verbose_name_plural = "Блюда_Ингриденты"

