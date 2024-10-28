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

class CustomUserLoginAPIView(APIView):
    permission_classes = [AllowAny]

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