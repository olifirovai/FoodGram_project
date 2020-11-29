from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('recipes/', include('recipe.urls')),
    path('', include('user.urls')),

]
