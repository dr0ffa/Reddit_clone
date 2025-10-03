import grpc
from grpc import aio
from sqlalchemy import select

from generated_proto import auth_pb2, auth_pb2_grpc
from models.database import get_db_context
from models.models_db import Users
from core.hash_password import hash_password, verify_password


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    async def RegisterUser(self, request, context):
        async with get_db_context() as db:
            if request.password != request.repeat_password:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Passwords do not match")

            result = await db.execute(select(Users).filter(Users.username == request.username))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, "Username already exists")

            new_user = Users(
                username=request.username,
                hashed_password=hash_password(request.password),
                email=request.email
            )

            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

        return auth_pb2.RegisterUserResponse(
            success=True,
            access_token="access_token_sample",
            refresh_token="refresh_token_sample",
            message="User registered successfully",
            # user_id=str(new_user.id)
        )

    async def LoginUser(self, request, context):
        return auth_pb2.LoginUserResponse(
            success=True,
            access_token="access_token_sample",
            refresh_token="refresh_token_sample",
            message="Login successful"
        )

    async def ValidateToken(self, request, context):
        return auth_pb2.TokenResponse(
            valid=True,
            user_id="user_001",
            message="Token is valid"
        )

    async def SendVerifyCode(self, request, context):
        return auth_pb2.SendVerifyCodeResponse(
            success=True,
            message="Verification code sent"
        )

    async def CheckVerifyCode(self, request, context):
        return auth_pb2.CheckVerifyCodeResponse(
            success=True,
            message="Verification code is correct"
        )


async def serve():
    server = aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    await server.start()
    print("Auth Service running on port 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    import asyncio
    asyncio.run(serve())
