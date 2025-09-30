from fastapi import APIRouter, Response, Request
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, RequestToken
from datetime import timedelta


from API_gateway.schemas.auth_schemas import RegisterUserRequest, AuthUserRequest
from API_gateway.utils.errors import handle_grpc_error
from API_gateway.grpc_client import register_user
from API_gateway.core.auth_config import security

from auth_service.core.config import settings
#from auth_service.core.hash_password import hash_password, verify_password
#from auth_service.models.models_db import Users, Mfa
#from auth_service.models.database import get_db

import grpc


auth_router = APIRouter(
    prefix=settings.api.prefix + settings.api.v1.prefix,
    tags=["auth"],
)


@auth_router.post("/register")
async def register(request: RegisterUserRequest):
    try:
        grpcResponse = register_user(
            username=request.username,
            email=request.email, 
            password=request.password, 
            repeat_password=request.repeat_password
        )
        return {
            "message": grpcResponse.message,
            "user_id": grpcResponse.user_id
        }
    except grpc.RpcError as e: handle_grpc_error(e)


@auth_router.post("/login")
async def login(request: AuthUserRequest, response: Response, db: Session = Depends(get_db)):
    try:
        grpcResponse = register_user(
            username=request.username,
            email=request.email, 
            password=request.password, 
            repeat_password=request.repeat_password
        )
        return {
            "message": grpcResponse.message,
            "user_id": grpcResponse.user_id
        }
    except grpc.RpcError as e: handle_grpc_error(e)



    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user or not verify_password(request.password, str(user.hashed_password)):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if db.query(Mfa).filter(Mfa.user_id == user.id, Mfa.enabled == True).first():
        return {True} # не забыть подписать
    else:
        access_token = security.create_access_token(uid=str(user.id), expiry=timedelta(minutes=60))
        refresh_token = security.create_refresh_token(uid=str(user.id), subject="refresh", expiry=timedelta(days=30))

        security.set_access_cookies(access_token, response)
        security.set_refresh_cookies(refresh_token, response)

        return {"username": user, "post": request, "access_token": access_token, "refresh_token": refresh_token}

        
        
