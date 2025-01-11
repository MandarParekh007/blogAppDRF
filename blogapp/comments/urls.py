from django.urls import path
from .views import CommentView

urlpatterns = [
    path('blogs/comment/<int:pk>', CommentView.as_view())
]
