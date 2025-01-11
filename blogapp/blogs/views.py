from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Blogs, Tags ,Comments
from users.models import CustomUser
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

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
    
    def get(self, request, pk=None):
        # If `pk` is provided, fetch a specific blog
        if pk:
            user = get_object_or_404(CustomUser,id=pk)
            blogs = Blogs.objects.filter(author=user, isDraft=False)
        else:
            blogs = Blogs.objects.filter(isDraft=False)
        
            
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_blogs = paginator.paginate_queryset(blogs, request)

        blog_data = [
            {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'publish_date': blog.publish_date,
                'author': blog.author.username,
            }
            for blog in paginated_blogs
        ]

        return paginator.get_paginated_response(blog_data)

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
        
class SearchByFilters(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        # Fetch blogs for a specific user if `pk` is provided
        if pk:
            user = CustomUser.objects.get(id=pk)
            blogs = Blogs.objects.filter(author=user, isDraft=False)
        else:
            blogs = Blogs.objects.filter(isDraft=False)

        # Apply filters if query parameters are present
        title = request.data.get('title')
        author = request.data.get('author')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        content = request.data.get('content')
        tags = request.data.get('tags',[])  # Assume tags are sent as a list

        if title:
            blogs = blogs.filter(title__icontains=title)
        if author:
            blogs = blogs.filter(author__username__icontains=author)
        if start_date:
            blogs = blogs.filter(publish_date__gte=start_date)
        if end_date:
            blogs = blogs.filter(publish_date__lte=end_date)
        if content:
            blogs = blogs.filter(content__icontains=content)
        if tags:
            blogs = blogs.filter(tags__tag__in=tags).distinct()

        # Paginate the filtered blogs
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_blogs = paginator.paginate_queryset(blogs, request)

        # Serialize the paginated blogs
        blog_data = [
            {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'publish_date': blog.publish_date,
                'author': blog.author.username,
                'tags': [tag.tag for tag in blog.tags_set.all()],  # Assuming reverse relation to Tags
            }
            for blog in paginated_blogs
        ]

        return paginator.get_paginated_response(blog_data)
