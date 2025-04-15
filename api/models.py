from django.db import models

class ProcessRequest(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='PENDING')
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.created_at}"