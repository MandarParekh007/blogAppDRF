from django.urls import path
from .views import BlogViews, PublishDraftView, SearchByFilters

urlpatterns = [
    path('blogs/', BlogViews.as_view(), name='blogs'),
    path('blogs/publish_draft/', PublishDraftView.as_view(), name='publish_draft'),
    path('blogs/<int:pk>/', BlogViews.as_view(), name='blog-detail'),
    path('blogs/filter/<int:pk>', SearchByFilters.as_view())
]
