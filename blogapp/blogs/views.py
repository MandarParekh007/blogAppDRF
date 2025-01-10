from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Blogs, Tags
from rest_framework import status

class BlogViews(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create blogs
    
    def post(self, request):
        user = request.user
        data = request.data
        
        # Get the blog details
        title = data.get('title')
        content = data.get('content')
        tags_data = data.get('tags', [])  # Extract tags from request data
        
        # Create the blog instance
        blog = Blogs.objects.create(title=title, content=content, author=user)
        
        # Create tags and associate them with the blog
        for tag in tags_data:
            Tags.objects.create(tag=tag, blog_id=blog)
        
        return Response({
            'success': 'true',
            'message': 'Blog is created successfully',
            'blog': {
                'title': blog.title,
                'content': blog.content,
                'author': blog.author.username,
                'tags': tags_data,
            }
        }, status=status.HTTP_201_CREATED)
