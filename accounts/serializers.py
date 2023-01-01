from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import *


class SignUpSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model=User
        fields = ['email', 'username','password']

# override validate method to make sure email does not exist
    def validate(self, attrs):
        email_exists=User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('Email has already been taken')
        return super().validate(attrs) 

# override create method to hash password
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user   