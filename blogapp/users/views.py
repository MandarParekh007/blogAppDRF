from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    

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
