# app.py
from flask import Flask
from camera import init_camera
from routes_awb import create_awb_routes
from routes_stream import create_stream_routes

app = Flask(__name__)

# 初始化相機（含硬體 AWB 收斂檢測）
picam2 = init_camera()

# 註冊路由
app.register_blueprint(create_stream_routes(picam2))
app.register_blueprint(create_awb_routes(picam2))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
