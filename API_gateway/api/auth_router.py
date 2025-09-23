from fastapi import HTTPException, APIRouter, Depends, Response, Request
from auth_service.core.config import settings
from API_gateway.schemas import RegisterUserRequest


auth_router = APIRouter(
    prefix=settings.api.prefix + settings.api.v1.prefix,
    tags=["auth"],
)

@auth_router.post("/register")
async def register(request: RegisterUserRequest, response: Response):
    if request.password != request.repeat_password:
        raise HTTPException(status_code=400, detail="passwords do not match")
    try: grpcResponse = register_user(username=request.username, email=request.email, password=request.password, repeat_password=request.repeat_password)
    except grpc.RpcError as e: handle_grpc_error(e)