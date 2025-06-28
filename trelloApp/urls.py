from django.urls import path, include
from .views import BoardView, TaskView, LoginView, UserView, BoardDelete, TaskDelete, TaskUpdate

urlpatterns = [
    path('board/', BoardView.as_view(), name='board'), 
    path('board/<int:pk>/delete', BoardDelete.as_view(), name='board_delete'), 
    path('login/', LoginView.as_view(), name='login'),
    path('task/', TaskView.as_view(), name='task'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete', TaskDelete.as_view(), name='task_delete'),
    path('User/', UserView.as_view(), name='user'),

]
