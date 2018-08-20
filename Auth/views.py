from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


@api_view(['POST'])
def user_login(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(username=serializer.data['username'], password=serializer.data['password'])
        if user:
            token = Token.objects.get(user=user)
            group = user.groups.all()[0].name
            json = serializer.data
            json['token'] = token.key
            json['type'] = group
            return Response(json, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            try:
                group = Group.objects.get(name='user')
            except Group.DoesNotExist:
                group = Group.objects.create(name='user')
            user.groups.add(group)
            json = serializer.data
            json['token'] = token.key
            json['type'] = 'user'
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resolver_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            try:
                group = Group.objects.get(name='resolver')
            except Group.DoesNotExist:
                group = Group.objects.create(name='resolver')
            user.groups.add(group)
            json = serializer.data
            json['token'] = token.key
            json['type'] = 'resolver'
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
