from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import *
from .models import *
from django.urls import reverse
from django.conf import settings
from .serializers import *
import http.client
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging
import asyncio
from telegram import Bot
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

class CustomUserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomUserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = CustomUser.objects.get(phone_number=phone_number)
            profile = Profile.objects.get(user=user)

            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            work_position = profile.work_position
            if work_position == 'admin':
                role = 'admin'
            elif work_position == 'system_manager':
                role = 'manager'
            elif work_position == 'accountant':
                role = 'accountant'
            else:
                role = 'employee'

            access['role'] = role

            return Response({
                'access': str(access),
                'refresh': str(refresh),
                'role': role,
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        if request.user.profile.work_position != 'admin':
            return Response({"error": "Only users with the 'admin' work position can create new users."},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully.", "user_id": user.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.create_reset_code()
            print(code)
            return Response({"detail": "Password reset code sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthenticatedPasswordResetRequestView(APIView):
    serializer_class = AuthenticatedPasswordResetRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuthenticatedPasswordResetRequestSerializer()
        code = serializer.create_reset_code(request.user)
        print(code)
        return Response({"detail": "Password reset code sent to your registered phone number."}, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'user': request.user if request.user.is_authenticated else None})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset  # Return all profiles for authenticated users

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = super().get_object()  # Get the profile instance
        # Allow only admin users to edit or delete profiles
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and self.request.user.profile.work_position != 'admin':
            raise permissions.PermissionDenied("You do not have permission to edit or delete this profile.")
        return profile