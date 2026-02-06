# FastAPI Development Skill

## Description
This skill provides expertise for developing applications using FastAPI, a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. This skill covers creating FastAPI applications, designing RESTful endpoints, implementing authentication systems, database integration, request/response validation, error handling, and deployment best practices.

Use this skill when working on:
- Creating new FastAPI applications from scratch
- Adding new endpoints to existing FastAPI applications
- Implementing authentication and authorization systems
- Integrating databases with FastAPI applications
- Setting up request/response validation
- Handling CORS and security configurations
- Implementing middleware and custom dependencies
- Creating API documentation with automatic schema generation
- Building production-ready FastAPI applications
- Optimizing FastAPI performance and scalability

## Parameters
- `app_structure`: Defines the recommended project structure for FastAPI applications
- `database_integration`: Options for integrating various databases (SQLAlchemy, Tortoise ORM, etc.)
- `authentication_methods`: Available authentication approaches (JWT, OAuth2, API keys)
- `validation_strategy`: Methods for request/response validation (Pydantic models, custom validators)
- `deployment_options`: Production deployment strategies (Uvicorn, Docker, cloud platforms)
- `testing_framework`: Testing tools and methodologies (pytest, TestClient)
- `middleware_config`: Configuration options for custom middleware
- `error_handling`: Error handling and logging strategies

## Usage Examples

### Creating a Basic FastAPI Application
```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### Adding Endpoints with Pydantic Models
```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item
```

### Implementing Authentication with JWT
```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Verify user exists in database
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user
```

### Database Integration with SQLAlchemy
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI

DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Custom Exception Handlers
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
```

## Implementation Details

### Best Practices for FastAPI Development

1. **Project Structure**:
   ```
   my_fastapi_app/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py          # Main application entry point
   │   ├── api/             # API routes
   │   │   ├── __init__.py
   │   │   └── v1/
   │   │       ├── __init__.py
   │   │       └── endpoints/
   │   │           ├── __init__.py
   │   │           ├── users.py
   │   │           └── items.py
   │   ├── models/          # Database models
   │   │   ├── __init__.py
   │   │   └── user.py
   │   ├── schemas/         # Pydantic models
   │   │   ├── __init__.py
   │   │   └── user.py
   │   ├── database.py      # Database setup
   │   └── config.py        # Configuration settings
   ├── tests/
   │   ├── __init__.py
   │   └── test_main.py
   ├── requirements.txt
   └── alembic/
       └── versions/
   ```

2. **Dependency Injection**:
   - Use FastAPI's dependency injection system for database connections, authentication, and other shared resources
   - Create reusable dependency functions that can be injected into multiple endpoints
   - Use `Depends()` to handle authentication, database sessions, and validation logic

3. **Request/Response Validation**:
   - Leverage Pydantic models for automatic request validation and serialization
   - Define input/output schemas separately for better maintainability
   - Use Pydantic's field constraints for additional validation rules

4. **Security Considerations**:
   - Implement proper authentication and authorization mechanisms
   - Use HTTPS in production environments
   - Validate and sanitize all user inputs
   - Implement rate limiting to prevent abuse
   - Use secure cookies and proper session management

5. **Performance Optimization**:
   - Use async/await for I/O-bound operations
   - Implement caching for frequently accessed data
   - Optimize database queries with proper indexing
   - Use connection pooling for database connections

6. **Testing**:
   - Write unit tests for individual functions
   - Write integration tests for API endpoints
   - Use FastAPI's TestClient for testing
   - Mock external services during testing

## Notes

- FastAPI automatically generates interactive API documentation (Swagger UI and ReDoc) at `/docs` and `/redoc` endpoints
- FastAPI is built on top of Starlette and Pydantic, leveraging their capabilities for high performance
- Type hints in FastAPI enable automatic request validation, response serialization, and OpenAPI schema generation
- FastAPI supports both async and sync functions, but async functions provide better performance for I/O-bound operations
- When deploying FastAPI applications, use ASGI servers like Uvicorn or Hypercorn rather than traditional WSGI servers
- FastAPI includes built-in support for dependency injection, which simplifies code organization and testing
- Always handle exceptions properly to avoid exposing internal errors to clients
- Use environment variables for configuration settings, especially sensitive information like database URLs and secret keys
- Consider using Alembic for database migrations when working with SQLAlchemy
- FastAPI's automatic validation and serialization reduce boilerplate code significantly compared to other frameworks