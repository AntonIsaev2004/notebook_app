from fastapi import FastAPI, Request, status, Depends
from src.auth.config import auth_backend, fastapi_users
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

from src.tasks.router import router as router_tasks


app = FastAPI(
    title="My App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_tasks)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"