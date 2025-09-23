from fastapi import HTTPException, APIRouter, Depends, Response, Request
from auth_service.core.config import settings
from API_gateway.schemas import RegisterUserRequest


auth_router = APIRouter(
    prefix=settings.api.prefix + settings.api.v1.prefix,
    tags=["auth"],
)

@auth_router.post("/register")
async def register(request: RegisterUserRequest, response: Response):
    