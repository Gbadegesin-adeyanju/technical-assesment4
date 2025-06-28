from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializers, TaskSerializer, BoardSerializer, UserSerializer
from django.contrib import auth
from .models import Board, Task
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound, PermissionDenied


# Create your views here.

class BoardView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def get(self, request):
        boards = Board.objects.filter(owner=request.user)
        serializer = self.serializer_class(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=BoardSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardDelete(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound("Board not found")

        if board.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this board.")

        board.delete()
        return Response({"message": "Board deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class TaskView(APIView):

    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request):
        task = Task.objects.filter(board__owner=request.user)
        serializer = self.serializer_class(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']  
            
            if board.owner != request.user:
                raise PermissionDenied("You do not own this board.")
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    
    @swagger_auto_schema(request_body=TaskSerializer)
    def put(self, request, pk=None): 
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound("Board not found")
        if board.owner != request.user:
            raise PermissionDenied("You do not own this board.")
        serializer = self.serializer_class(instance=board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class TaskDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound("Task not found")

        if task.board.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this board.")

        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializers)
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = auth.authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserView(APIView):

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
