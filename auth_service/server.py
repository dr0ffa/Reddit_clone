import grpc
from concurrent import futures
from generated_proto import auth_pb2, auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def LoginUser(self, request, context):
        print(f"Login attempt: {request.username}")
        return auth_pb2.RegisterUserResponse(
            success = True,
            access_token = "dfdf",
            refresh_token = "awewe",
            message = "hgfhg"
        )
    
    def Register(self, request, context):
        return auth_pb2.RegisterResponse(
            success=True, 
            user_id="user_001"
        )
    
    def VerifyToken(self, request, context):
        return auth_pb2.VerifyResponse(
            valid=True, 
            user_id="user_001"
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

