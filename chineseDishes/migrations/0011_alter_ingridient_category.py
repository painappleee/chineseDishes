# Generated by Django 5.1.2 on 2024-10-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chineseDishes', '0010_alter_ingridient_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingridient',
            name='category',
            field=models.CharField(choices=[('Мясо', 'Мясо'), ('Молочные продукты', 'Молочные продукты'), ('Крупы', 'Крупы')], max_length=30, verbose_name='Категория'),
        ),
    ]
