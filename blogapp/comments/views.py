from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from blogs.models import Blogs, Comments
from rest_framework.response import Response
from rest_framework import status

class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        comment = request.data.get('comment') 
        
        if not comment:
            return Response({
                'success': False,
                'message': 'Comment text is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        blog = get_object_or_404(Blogs, id=pk)

        comment = Comments.objects.create(comment=comment, blog_id=blog, user_id=user)

        return Response({
            'success': True,
            'message': 'Comment added successfully',
            'comment': {
                'comment': comment.comment,
                'commented_by': comment.user_id.username,
                'blog': comment.blog_id.title  
            }
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        user = request.user

        comment = Comments.objects.filter(id=pk, user_id=user)[0]
        blog = get_object_or_404(Blogs, id=comment.blog_id.id)

        if blog.author == user:
            comment.delete()
        else:
            return Response({
                'success' : False,
                'message' : "Can't delete the comment (UnAuthorized)"
            },status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'success' : True,
            'message' : 'comment deleted successfully'
        })

