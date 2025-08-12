# awb.py
import time
import threading
import numpy as np
from libcamera import controls

class AWBController:
    def __init__(self, picam2):
        self.picam2 = picam2
        self.prev_red_gain = 1.1
        self.prev_blue_gain = 0.9
        self.alpha = 0.3  # 平滑係數
        self.manual_mode = False

        threading.Thread(target=self._awb_loop, daemon=True).start()

    def _get_avg_rgb(self, frame):
        rgb = frame[..., ::-1]  # BGR → RGB
        return np.mean(rgb.reshape(-1, 3), axis=0)

    def _smooth_gain(self, rb_ratio):
        red_target = np.clip(np.interp(rb_ratio, [0.8, 1.5], [1.3, 0.9]), 0.8, 1.4)
        blue_target = np.clip(np.interp(rb_ratio, [0.8, 1.5], [0.8, 1.2]), 0.7, 1.3)
        red_gain = self.alpha * red_target + (1 - self.alpha) * self.prev_red_gain
        blue_gain = self.alpha * blue_target + (1 - self.alpha) * self.prev_blue_gain
        self.prev_red_gain, self.prev_blue_gain = red_gain, blue_gain
        return red_gain, blue_gain

    def _awb_loop(self):
        while True:
            if self.manual_mode:
                frame = self.picam2.capture_array()
                r, g, b = self._get_avg_rgb(frame)
                rb_ratio = r / (b + 1e-6)
                r_gain, b_gain = self._smooth_gain(rb_ratio)
                self.picam2.set_controls({
                    "ColourGains": (r_gain, b_gain),
                    "AwbMode": controls.AwbModeEnum.Custom
                })
                time.sleep(1)
            else:
                time.sleep(3)

    def enable_manual_awb(self):
        self.manual_mode = True
        print("[AWB] 已啟用自訂白平衡")

    def disable_manual_awb(self):
        self.manual_mode = False
        self.picam2.set_controls({
            "AwbEnable": True,
            "AwbMode": controls.AwbModeEnum.Auto
        })
        print("[AWB] 已切換回自動白平衡")

    def set_custom_gains(self, red_gain, blue_gain):
        self.enable_manual_awb()
        self.picam2.set_controls({
            "AwbMode": controls.AwbModeEnum.Custom,
            "ColourGains": (red_gain, blue_gain)
        })
