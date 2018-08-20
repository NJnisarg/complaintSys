from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        required=True
    )
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password')
