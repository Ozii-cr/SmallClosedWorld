from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from celery.result import AsyncResult
from .models import ProcessRequest
from .serializers import ProcessRequestSerializer, ProcessResponseSerializer, TaskStatusSerializer
from .tasks import process_request
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(
    description="Submit a new processing request",
    request=ProcessRequestSerializer,
    responses={
        202: ProcessResponseSerializer,
        400: {"description": "Invalid input"}
    },
    examples=[
        OpenApiExample(
            'Example Request',
            value={"email": "user@example.com", "message": "Please process this"},
            request_only=True
        ),
        OpenApiExample(
            'Example Response',
            value={"id": 1, "task_id": "test123", "status": "PENDING"},
            response_only=True
        )
    ]
)
class ProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ProcessRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Save the request to the database
            process_req = serializer.save()
            
            # Queue the task with Celery
            task = process_request.delay(
                process_req.id,
                serializer.validated_data['email'],
                serializer.validated_data['message']
            )
            
            # Update the task_id in the database
            process_req.task_id = task.id
            process_req.save()
            
            # Return the response with task_id
            response_serializer = ProcessResponseSerializer(process_req)
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    description="Check the status of a processing task",
    parameters=[
        OpenApiParameter(
            name='task_id',
            description='Celery Task ID',
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: TaskStatusSerializer,
        404: {"description": "Task not found"}
    }
)
class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        try:
            process_req = ProcessRequest.objects.get(task_id=task_id)
        except ProcessRequest.DoesNotExist:
            return Response(
                {"error": "Task not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get task status from Celery
        task_result = AsyncResult(task_id)
        
        response_data = {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.successful() else None
        }
        
        serializer = TaskStatusSerializer(data=response_data)
        serializer.is_valid()  
        
        return Response(serializer.data)