from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from auth_utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    fake_users_db,
    User
)

app = FastAPI(title="Todo API with JWT Authentication")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TokenRequest(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# Sample tasks data - replace with your actual database
sample_tasks = [
    Task(id=1, title="Sample task 1", completed=False),
    Task(id=2, title="Sample task 2", completed=True),
]

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: TokenRequest):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/api/user_1770462734589/tasks/", response_model=List[Task])
async def get_tasks(current_user: User = Depends(get_current_active_user)):
    """
    Protected endpoint that returns tasks for the authenticated user.
    """
    return sample_tasks

@app.post("/api/user_1770462734589/tasks/", response_model=Task)
async def create_task(task: Task, current_user: User = Depends(get_current_active_user)):
    """
    Protected endpoint to create a new task for the authenticated user.
    """
    sample_tasks.append(task)
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)