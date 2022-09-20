from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser,
    ]
