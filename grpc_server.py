from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUserInfo(self, request, context):
        # Simulated user data
        user_data = {1: ("Alice", 30), 2: ("Bob", 25)}
        name, age = user_data.get(request.user_id, ("Unknown", 0))
        return user_pb2.UserResponse(name=name, age=age)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
