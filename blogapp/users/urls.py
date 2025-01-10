from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, LoginApi

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('login/',LoginApi.as_view())
] + router.urls

