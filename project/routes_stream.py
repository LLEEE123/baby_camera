# routes_stream.py
from flask import Blueprint, Response
import cv2

def create_stream_routes(picam2):
    bp = Blueprint("stream_routes", __name__)

    def generate_frames():
        while True:
            frame = picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    @bp.route('/')
    def index():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return bp
