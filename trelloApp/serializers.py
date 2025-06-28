from rest_framework import serializers
from .models import Board, Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'board']

class BoardSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields =fields = ['title', 'owner', 'tasks']

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length = 150, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        # read_only_fields = ['username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
