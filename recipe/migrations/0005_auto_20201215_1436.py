# Generated by Django 3.1.3 on 2020-12-15 22:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_auto_20201215_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cook_time',
            field=models.PositiveSmallIntegerField(default=5, help_text='Add cook time in minutes', validators=[django.core.validators.MinValueValidator(1)], verbose_name='cook time'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='weight',
            field=models.PositiveSmallIntegerField(help_text='Add needed weight for the recipe', validators=[django.core.validators.MinValueValidator(1)], verbose_name='ingredient weight'),
        ),
    ]