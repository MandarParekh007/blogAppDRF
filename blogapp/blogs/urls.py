from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BlogViews


urlpatterns = [
    path('blogs/',BlogViews.as_view())
]

