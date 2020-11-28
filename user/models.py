from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''

    ADMIN = ('admin', 'admin',)
    USER = ('user', 'user',)


class User(AbstractUser):
    '''
    Creating the custom User model
    based on the AbstractUser model
    '''

    bio = models.TextField(max_length=200, blank=True,
                           verbose_name='user\'s biography',
                           help_text='Here You add Your bio')
    role = models.CharField(choices=UserRole.choices, default=UserRole.USER,
                            max_length=40, verbose_name='user\'s role')

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff or self.is_superuser

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.username
