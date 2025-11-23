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
model = YOLO("yolov8n.pt")  # Lightweight YOLOv8 nano model

# -----------------------------
# CAMERA SETUP
# -----------------------------
cap = cv2.VideoCapture(0)
last_sent = 0
SEND_INTERVAL = 10  # Minimum seconds between notifications

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)[0]
    humans_detected = []

    if results.boxes is not None:
        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            if int(cls) == 0:  # Class 0 is 'person'
                humans_detected.append((box, conf))
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'Person {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if humans_detected and (time.time() - last_sent > SEND_INTERVAL):
        filename = f"human_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        bot.send_photo(chat_id=CHAT_ID, photo=open(filename, 'rb'), caption="🚨 Human Detected!")
        last_sent = time.time()
        print(f"Notification sent! {len(humans_detected)} person(s) detected.")

    # Optional: display camera feed
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
cv2.destroyAllWindows()
