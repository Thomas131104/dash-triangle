from waitress import serve
from server import server

if __name__ == "__main__":
    print("🚀 Waitress đang phục vụ tại port 5000...")
    serve(server, host='0.0.0.0', port=5000)