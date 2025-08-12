# camera.py
from picamera2 import Picamera2
from libcamera import controls
import time

def init_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start()

    # 啟用硬體 AWB
    picam2.set_controls({
        "AwbEnable": True,
        "AwbMode": controls.AwbModeEnum.Auto,
        "Brightness": 0.0,
        "Contrast": 1.1,
        "Saturation": 1.1
    })

    # 等待硬體 AWB 收斂
    print("[Camera] 等待硬體 AWB 收斂中...")
    time.sleep(2)
    print("[Camera] 硬體 AWB 收斂完成")

    return picam2
