from fastapi import Request, Response, APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

@router.get("/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")

@router.get("/to_user")
def get_target_user(request: Request) -> Optional[str]:
    return request.cookies.get("X-TargetUser")


class RegisterValidator(BaseModel):
    username: str


@router.post("/register")
def register_user(user: RegisterValidator, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username)

@router.post("/pick_target")
def get_target(user:RegisterValidator, response: Response) -> None:
    response.set_cookie(key="X-TargetUser", value=user.username)