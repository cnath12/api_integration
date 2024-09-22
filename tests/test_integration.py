import unittest
import responses
import sqlite3
from api_client import BaseApiClient
from config import API_BASE_URL, AUTH_METHOD, AUTH_PARAMS
from db.database import DatabaseManager

class TestDatabaseManager(DatabaseManager):
    def __init__(self):
        self.connection = sqlite3.connect(':memory:')

    def connect(self):
        pass  # Already connected in __init__

    def close_connection(self):
        if self.connection:
            self.connection.close()

class TestApiClientIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = BaseApiClient(API_BASE_URL, AUTH_METHOD, AUTH_PARAMS)
        cls.client.db_manager = TestDatabaseManager()
        cls.client.db_manager.create_table("users")

    @classmethod
    def tearDownClass(cls):
        cls.client.db_manager.close_connection()

    def setUp(self):
        self.client.db_manager.connection.execute("DELETE FROM users")

    @responses.activate
    def test_get_users(self):
        responses.add(responses.GET, f"{API_BASE_URL}/users",
                      json={"data": [{"id": 1, "name": "John Doe", "email": "john@example.com"}]},
                      status=200)
        response = self.client.get("users")
        self.assertIsInstance(response, dict)
        self.assertIn("data", response)
        self.assertIsInstance(response["data"], list)

        # Check if user was added to the database
        cursor = self.client.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "John Doe")  # Assuming name is the second column

    @responses.activate
    def test_create_user(self):
        responses.add(responses.POST, f"{API_BASE_URL}/users",
                      json={"id": 2, "name": "Test User", "email": "test@example.com", "job": "Tester"},
                      status=201)
        new_user = {"name": "Test User", "email": "test@example.com", "job": "Tester"}
        response = self.client.post("users", data=new_user)
        self.assertIn("id", response)
        self.assertEqual(response["name"], "Test User")

        # Check if user was added to the database
        cursor = self.client.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", ("Test User",))
        user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[2], "test@example.com")  # Assuming email is the third column

    @responses.activate
    def test_update_user(self):
        responses.add(responses.PUT, f"{API_BASE_URL}/users/1",
                      json={"id": 1, "name": "John Doe", "email": "john@example.com", "job": "Senior Tester"},
                      status=200)
        update_data = {"job": "Senior Tester"}
        response = self.client.put("users/1", data=update_data)
        self.assertEqual(response["job"], "Senior Tester")

        # Check if user was updated in the database
        cursor = self.client.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
        user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[3], "Senior Tester")  # Assuming job is the fourth column

    @responses.activate
    def test_delete_user(self):
        # First, add a user
        self.client.db_manager.insert_user("users", {"id": 1, "name": "John Doe", "email": "john@example.com", "job": "Tester"})
        
        responses.add(responses.DELETE, f"{API_BASE_URL}/users/1",
                      status=204)
        response = self.client.delete("users/1")
        self.assertEqual(response.status_code, 204)

        # Check if user still exists in the database (it should, as we're not implementing cascade delete in this example)
        cursor = self.client.db_manager.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
        user = cursor.fetchone()
        self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()