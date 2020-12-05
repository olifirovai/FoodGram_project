from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('auth/logout/', LogoutView.as_view(),
         {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('my_friends/', views.follow_page, name='follow_page'),
    path('subscriptions', views.follow_author, name='subscription'),
    path('subscriptions/<int:id>', views.unfollow_author,
         name='unsubscription'),
    path('<username>/', views.user_profile, name='user_profile'),
]
