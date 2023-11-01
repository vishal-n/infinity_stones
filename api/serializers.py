from rest_framework import serializers
from .models import User, Stone, Activation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class StoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stone
        fields = ('id', 'stone_name')


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activation
        fields = ('id', 'user', 'stone', 'start_time', 'end_time')
