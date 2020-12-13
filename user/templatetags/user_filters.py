from django import template

from user.models import Follow

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter()
def is_following(author, user):
    follow = Follow.objects.get_follow(author, user)
    return follow


@register.filter()
def name_format(author):
    if author.last_name and author.first_name:
        return f'{author.first_name} {author.last_name}'
    return author.username
