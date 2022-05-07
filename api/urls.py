from django.contrib import admin
from django.urls import path,include
from . import views
from .views import URL_SHORTNER
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', views.short, name='index'),
    path('url/', URL_SHORTNER.as_view(), name='api'),
]
