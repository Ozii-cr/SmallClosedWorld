from rest_framework import serializers
from .models import ProcessRequest

class ProcessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessRequest
        fields = ['id', 'email', 'message', 'created_at', 'task_id', 'status']
        read_only_fields = ['created_at', 'task_id', 'status']

class ProcessResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessRequest
        fields = ['id', 'task_id', 'status']
        read_only_fields = ['id', 'task_id', 'status']

class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)
    result = serializers.CharField(allow_null=True)
