# Demo E-commerce App - User Servicesssss

This project demonstrates a simple e-commerce system built using a microservices architecture. It consists of one of the service used by this demo app:
**User Authentication Service**: Handles user registration and login, providing JWT tokens for authenticated sessions.

## Technology Stack

- Backend: Flask (Python)
- Database: MySQL
- Authentication: JWT

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

1. **Set up virtual environment (optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install dependencies**

Navigate to each service directory and install the required Python packages.

```bash
pip install -r requirements.txt
```

### Running the Services

#### Without Docker

Run the below command from the root path of the dir

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/defaultdb"
flask run --port=5000
```

> The application should be up and running on http://127.0.0.1:5000

#### With Docker

Run the below command from root path of the dir

```bash
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/defaultdb"
docker build -t ecomm-user-service .
docker run -e DATABASE_URL=$DATABASE_URL -p 5000:5000 ecomm-user-service
```

> The application should be up and running on http://127.0.0.1:5000

## API Endpoints

- **Register a User**

  - POST `/register`
  - Payload: `{"username": "testuser", "password": "password"}`

- **Log In**
  - POST `/login`
  - Payload: `{"username": "testuser", "password": "password"}`
  - Response: `{"access_token": "<JWT_Token>"}`

### Example Requests

1. **Register a User**

POST `http://localhost:5001/register`

Payload:

```json
{
  "username": "testuser",
  "password": "password"
}
```

2. **Log In**

POST `http://localhost:5001/login`

Payload:

```json
{
  "username": "testuser",
  "password": "password"
}
```

## Testing

To run unit tests for each service:

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/testdb"
python -m unittest discover tests
```
