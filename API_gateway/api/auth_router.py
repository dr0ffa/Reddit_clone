from fastapi import HTTPException, APIRouter, Depends, Response, Request
from auth_service.core.config import settings

from API_gateway.schemas import RegisterUserRequest
from API_gateway.utils import handle_grpc_error
from API_gateway.grpc_client import register_user

import grpc


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

    # set_auth_cookie(response, grpcResponse.access_token, grpcResponse.refresh_token)

    # return RegisterUserResponse(access_token=grpcResponse.access_token, refresh_token=grpcResponse.refresh_token, message=grpcResponse.message)