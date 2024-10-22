# Generated by Django 5.1.2 on 2024-10-22 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chineseDishes', '0018_alter_dish_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='province',
            name='area',
            field=models.PositiveIntegerField(verbose_name='Площадь(кв.км.)'),
        ),
        migrations.AlterField(
            model_name='province',
            name='population',
            field=models.PositiveIntegerField(verbose_name='Население(чел.)'),
        ),
    ]
