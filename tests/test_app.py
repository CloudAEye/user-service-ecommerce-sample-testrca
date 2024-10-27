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
        response = self.app.post('/register', json={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User registered successfully"})

    def test_02_login_user(self):
        response = self.app.post('/login', json={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    # Can add more tests here...

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestApp))