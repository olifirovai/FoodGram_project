from django.db import models


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
