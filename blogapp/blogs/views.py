from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Blogs, Tags ,Comments
from users.models import CustomUser
from rest_framework.pagination import PageNumberPagination

class BlogViews(APIView):
    permission_classes = [IsAuthenticated]  
    
    def post(self, request):
        user = request.user
        data = request.data
        
        # Get the blog details
        title = data.get('title')
        content = data.get('content')
        tags_data = data.get('tags', [])  # Extract tags from request data
        isDraft = data.get('isDraft', True)  # Default to draft
        publish_date = None

        if not isDraft:
            publish_date = now()
        
        # Create the blog instance
        blog = Blogs.objects.create(
            title=title, content=content, author=user, isDraft=isDraft, publish_date=publish_date
        )
        
        # Create tags and associate them with the blog
        for tag in tags_data:
            Tags.objects.create(tag=tag, blog_id=blog)
        
        return Response({
            'success': True,
            'message': 'Blog is created successfully',
            'blog': {
                'title': blog.title,
                'content': blog.content,
                'author': blog.author.username,
                'tags': tags_data,
                'draft': blog.isDraft
            }
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        user = request.user
        data = request.data

        try:
            # Fetch the blog instance
            blog = Blogs.objects.get(id=pk, author=user)

            # Update the blog details
            blog.title = data.get('title', blog.title)
            blog.content = data.get('content', blog.content)
            blog.isDraft = data.get('isDraft', blog.isDraft)
            blog.save()

            return Response({
                'success': True,
                'message': 'Blog updated successfully',
                'blog': {
                    'id': blog.id,
                    'title': blog.title,
                    'content': blog.content,
                    'isDraft': blog.isDraft,
                    'publish_date': blog.publish_date
                }
            }, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Blog not found or unauthorized access.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        user = request.user

        try:
            blog = Blogs.objects.filter(id=pk, author=user)

            if not blog:
                return Response({
                    'success': False,
                    'message': 'Blog does not exist'
                })
            
            blog.delete()

            return Response({
                'success' : True,
                'message' : 'Blog Deleted Successfully'
            })
        except Blogs.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Blog not found or unauthorized access.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        try:
            # Fetch the user by primary key
            user = CustomUser.objects.get(id=pk)
            # Fetch all blogs authored by the user
            blogs = Blogs.objects.filter(author=user,isDraft=False)

            paginator = PageNumberPagination()
            paginator.page_size = 1
            paginated_blogs = paginator.paginate_queryset(blogs, request) 
        
            # Serialize the blog data into a list of dictionaries
            blog_data = [
                {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'isDraft': blog.isDraft,
                'publish_date': blog.publish_date
                } for blog in paginated_blogs
            ]

            return paginator.get_paginated_response(blog_data)

        except CustomUser.DoesNotExist:
            return Response({
            'success': False,
            'message': 'User not found or unauthorized access'
        }, status=status.HTTP_404_NOT_FOUND)

class PublishDraftView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        blog_id = request.data.get('blog_id')

        try:
            # Fetch the draft blog authored by the user
            blog = Blogs.objects.get(id=blog_id, author=user, isDraft=True)
            blog.publish_date = now()
            blog.isDraft = False
            blog.save()

            return Response({
                'success': True,
                'message': 'Draft blog published successfully',
                'blog': {
                    'id': blog.id,
                    'title': blog.title,
                    'content': blog.content,
                    'author': blog.author.username,
                    'isDraft': blog.isDraft,
                }
            }, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Draft blog not found or unauthorized access.'
            }, status=status.HTTP_404_NOT_FOUND)
