from django.db import models

#TODO не думаю, что ради одной модели стоило заводить отдельное приложение.
# Тем более, что с ингридиентами сильно связаны рецепты.
# Это излишние дробление доменной области

class Ingredient(models.Model):
    name = models.CharField(max_length=5000, verbose_name='ingredient\'s name',
                            unique=True)
    measure = models.CharField(max_length=100, verbose_name='measurement unit')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measure})'
