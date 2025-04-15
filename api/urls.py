from django.urls import path
from . import views

urlpatterns = [
    path('process', views.ProcessAPIView.as_view(), name='process'),
    path('status/<str:task_id>', views.TaskStatusAPIView.as_view(), name='task_status'),
]