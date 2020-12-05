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

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.username


class FollowManager(models.Manager):
    def get_follow(self, author, user):
        return self.get_queryset().filter(author=author, user=user)

    def get_follow_list(self, user):
        return self.get_queryset().filter(author__following__user=user)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    objects = FollowManager()

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Followers'

    def __str__(self):
        return f'follower - {self.user} following - {self.author}'
