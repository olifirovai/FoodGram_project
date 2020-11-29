from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('auth/logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('my_friends/', views.follow_page, name='follow_page'),
    path('<username>/', views.user_profile, name='user_profile'),
]
