# routes_awb.py
from flask import Blueprint
from libcamera import controls
from awb import AWBController

def create_awb_routes(picam2):
    bp = Blueprint("awb_routes", __name__)
    awb = AWBController(picam2)

    @bp.route('/set_awb/<mode>')
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
            awb.disable_manual_awb()
            return f"已切換白平衡模式為 {mode}"
        elif mode == "Custom":
            awb.enable_manual_awb()
            return "已啟用自訂白平衡"
        else:
            return f"模式 {mode} 不存在，可用模式：{list(mode_map.keys()) + ['Custom']}"

    @bp.route('/set_color/<float:brightness>/<float:contrast>/<float:saturation>')
    def set_color(brightness, contrast, saturation):
        picam2.set_controls({
            "Brightness": brightness,
            "Contrast": contrast,
            "Saturation": saturation
        })
        return f"已設定 Brightness={brightness}, Contrast={contrast}, Saturation={saturation}"

    @bp.route('/set_custom_gains/<float:red_gain>/<float:blue_gain>')
    def set_custom_gains(red_gain, blue_gain):
        awb.set_custom_gains(red_gain, blue_gain)
        return f"已設定自訂白平衡增益：紅色={red_gain}, 藍色={blue_gain}"

    return bp
