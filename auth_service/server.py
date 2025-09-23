import grpc
from concurrent import futures
from auth_service.generated_proto import auth_pb2, auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def RegisterUser(self, request, context):
        return auth_pb2.RegisterUserResponse(
            success=True,
            access_token="access_token_sample",
            refresh_token="refresh_token_sample",
            message="User registered successfully"
        )

    def LoginUser(self, request, context):
        return auth_pb2.LoginUserResponse(
            success=True,
            access_token="access_token_sample",
            refresh_token="refresh_token_sample",
            message="Login successful"
        )

    def ValidateToken(self, request, context):
        return auth_pb2.TokenResponse(
            valid=True,
            user_id="user_001",
            message="Token is valid"
        )

    def SendVerifyCode(self, request, context):
        return auth_pb2.SendVerifyCodeResponse(
            success=True,
            message="Verification code sent"
        )

    def CheckVerifyCode(self, request, context):
        return auth_pb2.CheckVerifyCodeResponse(
            success=True,
            message="Verification code is correct"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Auth Service running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()