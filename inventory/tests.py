# Create your tests here.
# inventory/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import InventoryItem


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        # Test successful user registration
        data = {
            "username": "testuser221",
            "email": "testuser212@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully!")

    def test_user_registration_fail(self):
        # Test registration with missing data (should fail)
        data = {
            "username": "",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_login_success(self):
        # Test successful login
        data = {"username": "testuser221", "password": "testpassword"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_fail(self):
        # Test login with incorrect credentials
        data = {"username": "testuser221", "password": "wrongpassword"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_item_success(self):
        # Test successful item creation
        data = {
            "name": "Laptop",
            "description": "A powerful laptop",
            "quantity": 10,
            "price": 999.99,
        }
        response = self.client.post(reverse("create-item"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Laptop")

    def test_create_item_fail(self):
        # Test item creation with invalid data
        data = {
            "name": "",  # Name is missing
            "description": "A powerful laptop",
            "quantity": 10,
            "price": 999.99,
        }
        response = self.client.post(reverse("create-item"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.item = InventoryItem.objects.create(
            name="Laptop", description="A powerful laptop", quantity=10, price=999.99
        )

    def test_get_item_success(self):
        # Test successful item fetch
        response = self.client.get(
            reverse("get-item", kwargs={"item_id": self.item.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")

    def test_get_item_not_found(self):
        # Test item not found
        response = self.client.get(
            reverse("get-item", kwargs={"item_id": 999})
        )  # Non-existing ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.item = InventoryItem.objects.create(
            name="Laptop", description="A powerful laptop", quantity=10, price=999.99
        )

    def test_update_item_success(self):
        # Test successful item update
        data = {
            "name": "Updated Laptop",
            "description": "An even more powerful laptop",
            "quantity": 5,
            "price": 1099.99,
        }
        response = self.client.put(
            reverse("update-item", kwargs={"item_id": self.item.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Laptop")

    def test_update_item_not_found(self):
        # Test update for a non-existing item
        data = {
            "name": "Non-existing Laptop",
            "description": "Non-existent",
            "quantity": 5,
            "price": 1099.99,
        }
        response = self.client.put(
            reverse("update-item", kwargs={"item_id": 999}), data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.item = InventoryItem.objects.create(
            name="Laptop", description="A powerful laptop", quantity=10, price=999.99
        )

    def test_delete_item_success(self):
        # Test successful item deletion
        response = self.client.delete(
            reverse("delete-item", kwargs={"item_id": self.item.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Item deleted successfully")

    def test_delete_item_not_found(self):
        # Test deletion of non-existing item
        response = self.client.delete(
            reverse("delete-item", kwargs={"item_id": 999})
        )  # Non-existing ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllItemsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        InventoryItem.objects.create(
            name="Laptop", description="A powerful laptop", quantity=10, price=999.99
        )
        InventoryItem.objects.create(
            name="Smartphone", description="Latest smartphone", quantity=5, price=699.99
        )

    def test_get_all_items_success(self):
        # Test fetching all items
        response = self.client.get(reverse("get-all-items"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 items
