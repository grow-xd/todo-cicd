from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ToDo

class ToDoTests(APITestCase):

    def setUp(self):
        self.todo = ToDo.objects.create(title="Test Task", description="Test Description", completed=False)
        self.todo_url = reverse('todo-detail', kwargs={'pk': self.todo.pk})
        self.todos_url = reverse('todo-list')

    def test_create_todo(self):
        url = self.todos_url
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "completed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDo.objects.count(), 2)
        self.assertEqual(ToDo.objects.get(id=2).title, 'New Task')

    def test_list_todos(self):
        url = self.todos_url
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_todo(self):
        url = self.todo_url
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.todo.title)

    def test_update_todo(self):
        url = self.todo_url
        data = {
            "title": "Updated Task",
            "description": "Updated Task Description",
            "completed": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Task')
        self.assertEqual(self.todo.completed, True)

    def test_partial_update_todo(self):
        url = self.todo_url
        data = {
            "completed": True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.completed, True)

    def test_delete_todo(self):
        url = self.todo_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ToDo.objects.count(), 0)
