import os
import uvicorn
import atexit
from fastapi import FastAPI
from api import routes
import py_eureka_client.eureka_client as eureka_client

app = FastAPI()
app.include_router(routes.router)

# Eureka server configuration
EUREKA_SERVER = "http://localhost:8761/eureka/"
APP_NAME = "fastapi-service"
INSTANCE_PORT = 8000

def register_with_eureka():
    eureka_client.init(
        eureka_server=EUREKA_SERVER,
        app_name=APP_NAME,
        instance_port=INSTANCE_PORT,
        instance_host=os.getenv('HOST', 'localhost'),
        instance_ip=os.getenv('IP', '127.0.0.1')
    )
    
def deregister_from_eureka():
    try:
        print("Deregistering from Eureka...")
        eureka_client.stop()
    except Exception as e:
        print(f"Error during deregistration: {e}")

if __name__ == "__main__":
    register_with_eureka()
    atexit.register(deregister_from_eureka)
    uvicorn.run(app, host="0.0.0.0", port=INSTANCE_PORT)