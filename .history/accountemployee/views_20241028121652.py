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