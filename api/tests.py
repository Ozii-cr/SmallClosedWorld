from django.test import TestCase
from .models import ProcessRequest
from .tasks import process_request


# Create your tests here.
class ModelTests(TestCase):

    def test_process_request_model(self):
        process_req = ProcessRequest.objects.create(
            email="info@smallclosedworld.com",
            message="Testing",
            task_id="test123",
            status="PENDING"
        )
        
        # Check if it was created properly
        self.assertEqual(process_req.email, "info@smallclosedworld.com")
        self.assertEqual(process_req.message, "Testing")
        self.assertEqual(process_req.task_id, "test123")
        self.assertEqual(process_req.status, "PENDING")


class TaskTests(TestCase):

    def test_process_request_task(self):
        """Test the process_request task works correctly."""
        # Create a process request in the database
        process_req = ProcessRequest.objects.create(
            email="info@smallclosedworld.com",
            message="Testing",
            task_id="Test123"
        )
        
        # Run the task directly, not through celery
        result = process_request(process_req.id, process_req.email, process_req.message)
    
        process_req.refresh_from_db()
        
        # Check the result
        self.assertIn("Processed message for info@smallclosedworld.com", result)
        self.assertEqual(process_req.status, "COMPLETED")
        self.assertEqual(process_req.result, result)