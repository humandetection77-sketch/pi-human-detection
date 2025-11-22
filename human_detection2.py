import cv2
import time
import yagmail
from ultralytics import YOLO

# --- EMAIL SETUP ---
SENDER_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"  # Gmail app password
RECIPIENT_EMAIL = "your_iphone_email@icloud.com"

yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)

def send_notification(image_path):
    print("Sending email notification...")
    yag.send(
        to=RECIPIENT_EMAIL,
        subject="🚨 Human Detected!",
        contents="A person has appeared on your camera.",
        attachments=image_path
    )
    print("Notification sent!")

# --- LOAD YOLO MODEL ---
model = YOLO("yolov8n.pt")  # lightweight YOLOv8 nano model

# --- CAMERA SETUP ---
cap = cv2.VideoCapture(0)

last_sent = 0
SEND_INTERVAL = 10  # seconds between notifications

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)[0]  # Run detection on current frame

    humans_detected = False

    # Loop through detections
    for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
        if int(cls) == 0:  # Class 0 is "person"
            humans_detected = True
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f'Person {conf:.2f}', (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    # Send notification if human detected and cooldown passed
    if humans_detected and (time.time() - last_sent > SEND_INTERVAL):
        filename = f"human_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        send_notification(filename)
        last_sent = time.time()

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
