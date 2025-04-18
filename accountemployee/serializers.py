from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from .utils import *

class CustomUserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("Invalid phone number or password.")
        else:
            raise serializers.ValidationError("Both 'phone_number' and 'password' are required.")

        data['user'] = user
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.JSONField(write_only=True)  # Add profile as a nested field

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'full_name', 'email', 'password', 'profile')

    def create(self, validated_data):
        # Extract profile data
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')

        # Create user
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create profile linked to user
        Profile.objects.create(user=user, **profile_data)
        
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number does not exist.")
        return value

    def create_reset_code(self):
        user = CustomUser.objects.get(phone_number=self.validated_data['phone_number'])
        code = random.randint(100000, 999999)
        PasswordResetCode.objects.create(user=user, code=str(code))
        to = [self.validated_data['phone_number'],]
        message = str(code)
        send_sms(to,message) 
        return code

class AuthenticatedPasswordResetRequestSerializer(serializers.Serializer):
    def create_reset_code(self, user):
        code = random.randint(100000, 999999)
        PasswordResetCode.objects.create(user=user, code=str(code))
        to = [user.profile.phone_number,]
        send_sms(to,str(code))
        return code

class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=False)
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        user = self.context.get('user')
        
        if not user and phone_number:
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except user.DoesNotExist:
                raise serializers.ValidationError("User with this phone number does not exist.")
        
        reset_code = PasswordResetCode.objects.filter(user=user, code=data['code']).last()
        if reset_code is None or reset_code.is_expired():
            raise serializers.ValidationError("Invalid or expired reset code.")
        
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        PasswordResetCode.objects.filter(user=user).delete()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['work_position', 'department', 'date_of_assignment']