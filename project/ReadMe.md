# Raspberry Pi Camera with AWB Control

本專案是一個基於 **Flask + Picamera2** 的樹莓派攝影機網路串流伺服器，  
支援：
- 即時影像串流（MJPEG）
- 硬體白平衡（AWB）控制
- 自訂白平衡演算法（灰世界 + 平滑過渡）
- 即時色彩調整（亮度、對比、飽和度）

---

## 📂 專案架構

project/
├─ app.py # 主 Flask 啟動與註冊路由
├─ camera.py # 相機初始化與基本控制（含硬體 AWB 收斂檢測）
├─ awb.py # 白平衡演算法與控制
├─ routes_awb.py # 白平衡與色彩 API
└─ routes_stream.py # 影像串流 API


---

## 🚀 安裝與執行

### 1️⃣ 安裝必要套件
sudo apt update
sudo apt install -y python3-pip python3-opencv
pip3 install flask picamera2 numpy

### 2️⃣ 啟動程式
bash
複製
編輯
python3 app.py
啟動後伺服器會在 http://樹莓派IP:8080/ 運行。

## 🌐 API 說明
影像串流
GET /
取得即時 MJPEG 串流。

設定白平衡模式
GET /set_awb/<mode>
可用模式：
Auto
Daylight
Cloudy
Tungsten
Fluorescent
Custom（啟用自訂白平衡演算法）

範例：
GET /set_awb/Tungsten
設定影像色彩參數
GET /set_color/<brightness>/<contrast>/<saturation>
brightness: -1.0 ~ 1.0
contrast: 0.0 ~ 2.0
saturation: 0.0 ~ 2.0

範例：
GET /set_color/0.0/1.2/1.1
設定自訂白平衡增益
GET /set_custom_gains/<red_gain>/<blue_gain>
red_gain: 0.5 ~ 2.0
blue_gain: 0.5 ~ 2.0

範例：
GET /set_custom_gains/1.3/0.9


## ⚙️ 開機流程
初始化相機（camera.py）
啟用硬體 AWB
等待 2 秒收斂
啟動 Flask 伺服器（app.py）
API 控制白平衡與色彩（routes_awb.py）
MJPEG 即時串流（routes_stream.py）

📌 注意事項
請確保樹莓派啟用 libcamera 並能正常使用 libcamera-hello
如果使用自訂白平衡（Custom），系統會自動啟用 awb.py 中的演算法進行即時調整
camera.py 的硬體 AWB 收斂檢測可依需求調整等待時間（預設 2 秒）