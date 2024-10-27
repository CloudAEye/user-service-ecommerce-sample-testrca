import unittest

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.models import User
from src.service import UserService


class TestUserService(unittest.TestCase):
    service = UserService()
    username = "test_service@cloudaeye.com"
    password = "Admin@1234"

    @classmethod
    def setUpClass(cls):
        print("setting up")
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        print("tearing down")
        with app.app_context():
            cls.service.delete_user(cls.username)

    def test_01_register_success(self):
        with app.app_context():
            result = self.service.register({
                "username": self.username,
                "password": self.password
            })
            self.assertEqual(result, 'User registered successfully')

    def test_02_register_user_already_exists(self):
        # Try registering a user with the same username
        data = {'username': self.username, 'password': self.password}
        with app.app_context():
            with self.assertRaises(Exception) as context:
                self.service.register(data)
            self.assertEqual(str(context.exception), 'Username already taken')

    def test_03_login_success(self):
        # Attempt to log in with correct credentials
        data = {'username': self.username, 'password': self.password}
        with app.app_context():
            result: User = self.service.login(data)
            self.assertEqual(result.username, self.username)

    def test_login_invalid_username(self):
        # Attempt to log in with a username that does not exist
        data = {'username': 'nonexistent', 'password': self.password}
        with app.app_context():
            with self.assertRaises(Exception) as context:
                self.service.login(data)
        self.assertEqual(str(context.exception), 'Invalid username or password')

    def test_login_invalid_password(self):
        # Attempt to log in with a username that does not exist
        data = {'username': self.username, 'password': "wrongpassword"}
        with app.app_context():
            with self.assertRaises(Exception) as context:
                self.service.login(data)
        self.assertEqual(str(context.exception), 'Invalid username or password')


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestUserService))
