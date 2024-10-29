from flask import Flask, jsonify, request
import grpc
import user_pb2
import user_pb2_grpc

app = Flask(__name__)

def get_user_info(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        user_request = user_pb2.UserRequest(user_id=user_id)
        return stub.GetUserInfo(user_request)


@app.route("/")
def root():
    return "Root path..."
    

@app.route("/user/<int:user_id>")
def user_info(user_id):
    try:
        response = get_user_info(user_id)
        return jsonify({"name": response.name, "age": response.age})
    except grpc.RpcError as e:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)
