# Quiz API

A FastAPI-based quiz application with PostgreSQL database support. This API provides endpoints for managing quiz categories, questions, and user authentication.

## Features

- User authentication with JWT tokens
- Admin dashboard for managing categories and questions
- Four predefined categories: Countries, Animals, Programming, and Cyber Security
- RESTful API endpoints for all operations
- PostgreSQL database integration
- CORS support for web and mobile applications

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd quiz-api
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
- Create a new database named `quiz_db`
- Update the `DATABASE_URL` in `config.py` with your PostgreSQL credentials

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /token` - Get access token
- `POST /users/` - Create new user

### Categories
- `POST /categories/` - Create new category (Admin only)
- `GET /categories/` - Get all categories

### Questions
- `POST /questions/` - Create new question (Admin only)
- `GET /questions/` - Get all questions
- `GET /questions/{question_id}` - Get specific question

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Admin-only endpoints for content management
- CORS enabled for cross-origin requests

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 