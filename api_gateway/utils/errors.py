from fastapi import HTTPException, status
import grpc


def handle_grpc_error(error: grpc.RpcError):
    error_message = error.details()

    status_map = {
        grpc.StatusCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
        grpc.StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        grpc.StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        grpc.StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        grpc.StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
        grpc.StatusCode.RESOURCE_EXHAUSTED: status.HTTP_429_TOO_MANY_REQUESTS,
        grpc.StatusCode.UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
        grpc.StatusCode.INTERNAL: status.HTTP_500_INTERNAL_SERVER_ERROR
    }

    raise HTTPException(
        status_code=status_map.get(error.code(), status.HTTP_500_INTERNAL_SERVER_ERROR),
        detail=error_message
    )