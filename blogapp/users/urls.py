from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, LoginApi

# router = SimpleRouter()
# router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('users/',UserViewSet.as_view()),
    path('users/<int:pk>',UserViewSet.as_view()),
    path('login/',LoginApi.as_view())
] 

