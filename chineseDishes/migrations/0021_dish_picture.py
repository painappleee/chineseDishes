# Generated by Django 5.1.2 on 2024-11-19 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chineseDishes', '0020_remove_dish_ingridients'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='picture',
            field=models.ImageField(null=True, upload_to='chineseDishes', verbose_name='Изображение'),
        ),
    ]