from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import controls
import cv2

app = Flask(__name__)

# 初始化 Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# 預設參數
picam2.set_controls({
    "AwbEnable": True,
    "AwbMode": controls.AwbModeEnum.Auto,
    "Brightness": 0.0,
    "Contrast": 1.1,
    "Saturation": 1.1
})

def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 即時切換白平衡模式
@app.route('/set_awb/<mode>')
def set_awb(mode):
    mode_map = {
        "Auto": controls.AwbModeEnum.Auto,
        "Daylight": controls.AwbModeEnum.Daylight,
        "Cloudy": controls.AwbModeEnum.Cloudy,
        "Tungsten": controls.AwbModeEnum.Tungsten,
        "Fluorescent": controls.AwbModeEnum.Fluorescent
    }
    if mode in mode_map:
        picam2.set_controls({"AwbMode": mode_map[mode]})
        return f"已切換白平衡模式為 {mode}"
    else:
        return f"模式 {mode} 不存在，可用模式：{list(mode_map.keys())}"

# 即時調整顏色參數
@app.route('/set_color/<float:brightness>/<float:contrast>/<float:saturation>')
def set_color(brightness, contrast, saturation):
    picam2.set_controls({
        "Brightness": brightness,
        "Contrast": contrast,
        "Saturation": saturation
    }) 
    return f"已設定 Brightness={brightness}, Contrast={contrast}, Saturation={saturation}"

# 即時調整白平衡增益
@app.route('/set_custom_gains/<float:red_gain>/<float:blue_gain>')
def set_custom_gains(red_gain, blue_gain):
    picam2.set_controls({
        "AwbMode": controls.AwbModeEnum.Custom,
        "ColourGains": (red_gain, blue_gain)
    })
    return f"已設定自訂白平衡增益：紅色={red_gain}, 藍色={blue_gain}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
