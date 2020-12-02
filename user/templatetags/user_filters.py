from django import template

from user.models import Follow

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='check_following')
def check_following(author, user):
    follow = Follow.objects.get_follow(author, user)
    return follow
