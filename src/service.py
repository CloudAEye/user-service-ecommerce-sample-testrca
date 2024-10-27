from src.models import User, db


class UserService:
    def register(self, data):
        """
        Registers a new user with the given payload
        :param data: Data of the new user
        :return: Success message
        """
        user = User.query.filter_by(username=data['username']).first()
        if user:
            raise Exception('Username already taken')
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return 'User registered successfully'

    def delete_user(self, username):
        """
        Registers a new user with the given payload
        :param data: Data of the new user
        :return: Success message
        """
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def login(self, data):
        """
        Logs in user with the given details
        :param data: Details of the user
        :return: Logged in user details
        """
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return user
        raise Exception('Invalid username or password')
