from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
import grpc_reflection.v1alpha.reflection as grpc_reflection

import schemas.users_pb2 as users_pb2


@asynccontextmanager
async def grpc_lifespan(app: FastAPI):
    yield


SERVICE_NAMES = (
    users_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
    grpc_reflection.SERVICE_NAME,
)


class UserRequest(BaseModel):
    data: str
    # data: CreateUserRequest


users_db: list[UserRequest] = []
app = FastAPI()


@app.get("/users")
async def get_user():
    return UserRequest(data="hello")


@app.post("/users")
async def create_user(user: CreateUserRequest):
    users_db.append(user)


@app.get("/users/list")
async def get_users() -> list[UserRequest]:
    return users_db
