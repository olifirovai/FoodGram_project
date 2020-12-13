# Generated by Django 3.1.3 on 2020-12-11 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20201211_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipetype',
            name='type_name',
            field=models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], max_length=25, unique=True),
        ),
    ]
