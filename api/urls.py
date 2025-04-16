from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views

urlpatterns = [
    path('process', views.ProcessAPIView.as_view(), name='process'),
    path('status/<str:task_id>', views.TaskStatusAPIView.as_view(), name='task_status'),
    
    #api documentation
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]