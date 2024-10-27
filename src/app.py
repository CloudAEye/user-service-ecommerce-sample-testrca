from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from src.models import db
from src.service import UserService

app = Flask(__name__)

# Configuration
app.config.from_pyfile('config.py')

# Extensions
db.init_app(app)
jwt = JWTManager(app)


# Create the database tables before the first request
@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

# Routes
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        user_service = UserService()
        result = user_service.register(data=data)
        return jsonify({'message': result}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user_service = UserService()
        user = user_service.login(data=data)
        expires = timedelta(hours=1)
        access_token = create_access_token(identity=user.username, expires_delta=expires)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
