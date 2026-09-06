from django.test import TestCase, Client
from rag1.models import User, Task
import json

class TaskBoardAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(Username="testuser", Password="password123")
        self.task = Task.objects.create(
            Title="Test Task",
            Description="Description",
            completed=False,
            user_id=self.user.id
        )

    def test_api_register(self):
        response = self.client.post(
            "/api/register",
            data=json.dumps({"username": "newuser", "password": "pass", "confirm": "pass"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("user", response.json())

    def test_api_login(self):
        response = self.client.post(
            "/api/login",
            data=json.dumps({"username": "testuser", "password": "password123"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["username"], "testuser")

    def test_api_create_task(self):
        response = self.client.post(
            f"/api/tasks/{self.user.id}/create",
            data=json.dumps({"title": "New Task", "description": "Details", "completed": False, "priority": "High", "due_date": "2026-09-10"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()["tasks"]), 2)
        created = response.json()["tasks"][-1]
        self.assertEqual(created["priority"], "High")
        self.assertEqual(created["due_date"], "2026-09-10")

    def test_api_update_task(self):
        response = self.client.post(
            f"/api/tasks/{self.task.id}/update",
            data=json.dumps({"title": "Updated Task", "description": "Updated", "completed": True, "priority": "Low", "due_date": "2026-09-12"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.Title, "Updated Task")
        self.assertTrue(self.task.completed)
        self.assertEqual(self.task.priority, "Low")

    def test_api_toggle_task(self):
        response = self.client.post(
            f"/api/tasks/{self.task.id}/toggle",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_api_delete_task(self):
        response = self.client.post(
            f"/api/tasks/{self.task.id}/delete",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_react_app_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "./app.html")

