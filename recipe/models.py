import random
import string

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField

from ingredients.models import Ingredient
from user.models import User


class Types(models.TextChoices):
    '''

    '''
    BREAKFAST = ('breakfast', 'breakfast',)
    LUNCH = ('lunch', 'lunch',)
    DINNER = ('dinner', 'dinner',)


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='recipe\'s name')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    type = MultiSelectField(choices=Types.choices, default=Types.LUNCH)
    directions = models.TextField()
    post_date = models.DateTimeField(auto_now=True, db_index=True,
                                     verbose_name='publishing date')
    cook_time = models.IntegerField(
        verbose_name='cook time', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Add cook time in minutes'
    )
    picture = models.ImageField(verbose_name='picture of the recipe',
                                blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-post_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            random_mark = ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in
                range(6))
            self.slug = slugify(random_mark + '-' + self.name)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredient')
    weight = models.IntegerField(
        verbose_name='ingredient weight', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Add needed weight for the recipe'
    )

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipes Ingredients'
        ordering = ['recipe']
