import cv2
import time
from ultralytics import YOLO
from telegram import Bot

# -----------------------------
# TELEGRAM CONFIG
# -----------------------------
BOT_TOKEN = "7949112389:AAGEJd1ZBIGg-7m96mxqGZLsBa7kub6GXbo"
CHAT_ID = 5667037889  # Your Telegram chat ID
bot = Bot(token=BOT_TOKEN)

# -----------------------------
# YOLOv8 MODEL
# -----------------------------
model = YOLO("yolov8n.pt")  # Lightweight nano model

# -----------------------------
# CAMERA SETUP
# -----------------------------
cap = cv2.VideoCapture(0)
last_sent = 0
SEND_INTERVAL = 10  # Minimum seconds between messages

# -----------------------------
# MAIN LOOP (HEADLESS)
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)[0]

    # Check for humans (class 0)
    humans_detected = any(int(cls) == 0 for cls in results.boxes.cls) if results.boxes is not None else False

    # Send Telegram text message if human detected
    if humans_detected and (time.time() - last_sent > SEND_INTERVAL):
        bot.send_message(chat_id=CHAT_ID, text="🚨 Human Detected!")
        last_sent = time.time()
        print(f"Notification sent at {time.strftime('%H:%M:%S')}")

cap.release()
