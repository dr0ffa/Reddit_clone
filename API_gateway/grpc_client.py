import grpc
from auth_service.generated_proto.auth_pb2 import RegisterUserRequest, LoginUserRequest, SendVerifyCodeRequest
from auth_service.generated_proto.auth_pb2_grpc import AuthServiceStub


channel_grpc = grpc.insecure_channel("auth-service:50051")
auth_client = AuthServiceStub(channel_grpc)


def register_user(username: str, email: str, password: str, repeat_password: str):
    response = auth_client.RegisterUser(RegisterUserRequest(username=username, email=email, password=password, repeat_password=repeat_password))
    return response