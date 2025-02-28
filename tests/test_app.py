import random
import time
import unittest

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.models import User
from src.service import UserService


class TestApp(unittest.TestCase):
    service = UserService()
    username = "test_app@cloudaeye.com"
    password = "Admin@1234"

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            cls.service.delete_user(cls.username)

    def test_01_register_user(self):
        response = self.app.post(
            '/register', json={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json, {"message": "User registered successfully"})

    def test_02_login_user(self):
        response = self.app.post(
            '/login', json={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)


def test_03_flaky_test(self):
    """
    A flaky test that randomly passes or fails without code changes.
    """
    # Generate a random number between 0 and 1
    random_value = random.random()

    # Simulate a network delay
    time_to_sleep = random.uniform(0.1, 0.3)

    # Print debug information
    print(
        f"Flaky test random value: {random_value}, sleep time: {time_to_sleep}")

    # Introduce a small delay to simulate network latency
    time.sleep(time_to_sleep)

    # Test will fail approximately 50% of the time
    # This creates the flaky behavior without relying on external network calls
    self.assertTrue(
        random_value > 0.5,
        f"Flaky test failed with random value {random_value} (needed > 0.5)"
    )


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    # None to keep the method definition order
    test_loader.sortTestMethodsUsing = None
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestApp))
