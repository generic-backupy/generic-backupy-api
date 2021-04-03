from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'first_name', 'last_name', 'email', 'created_at', 'email_verified')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'created_at')

class UserShortListSerializer(serializers.ModelSerializer):

    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_admin')

class UserGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)
