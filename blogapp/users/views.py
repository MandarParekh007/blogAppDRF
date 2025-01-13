from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(APIView):
    def get_permissions(self):
        """
        Dynamically assign permissions based on the request method.
        """
        if self.request.method == 'POST':
            # No permission required for POST (user registration)
            return []
        return [IsAuthenticated()] 

    def post(self, request):
        self.permission_classes = []
        userdata = request.data
        user_details_ser = CustomUserSerializer(data=userdata)

        if user_details_ser.is_valid():
            user = user_details_ser.save()
            return Response({
                'success': True,
                'message': 'User Created Successfully',
                'user': {
                    'email': user.email,
                    'username': user.username,
                    'phone': user.phone
                }
            },status=status.HTTP_201_CREATED)
    
        return Response({
            'success':False,
            'message': user_details_ser.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            user = CustomUser.objects.filter(id=pk)[0]
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user can only update their own details
        if request.user != user:
            return Response({
                'detail': 'You do not have permission to update this user.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Update user details
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User updated successfully.',
                'user': serializer.data
            })

        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    

class LoginApi(APIView):
    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)
    
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            email = serializer.validated_data['email']  # Use validated_data
            password = serializer.validated_data['password']  # Use validated_data
            user = authenticate(email=email, password=password)
            
            if user is None:
                return Response({
                    'status': 404,
                    'message': 'Invalid email or password',
                    'data': {}
                })
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 200,
                'message': 'Login successful',
                'data': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            })

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })
    
    def get(self, request):
        """
        Provide the serializer fields in the browsable API for GET requests.
        """
        serializer = self.get_serializer()
        return Response(serializer.data)
