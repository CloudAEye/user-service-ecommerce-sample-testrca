import os
import random
import unittest
import subprocess

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.models import User
from src.service import UserService
import platform


class TestApp(unittest.TestCase):
    service = UserService()
    username = "test_app@.com"
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
        delay = random.uniform(0.2, 0.3)
        if platform.system().lower() == 'windows':
            ping_command = ['ping', '-n', '1', 'google.com']
        else:
            ping_command = ['ping', '-c', '1',
                            '-W', '1', 'https://www.google.com']
        try:
            result = subprocess.run(
                ping_command,
                capture_output=True,
                text=True,
                timeout=10  # Very short timeout
            )
            print("result", result)
            self.assertEqual(result.returncode, 0)
        except subprocess.TimeoutExpired:
            self.fail("Test failed due to timeout")

    # def test_randomly_flaky(self):
    #     # Randomly pass or fail the test (50/50 chance)
    #     self.assertTrue(random.choice(
    #         [True, False]), "Flaky test randomly failed")


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestApp))
