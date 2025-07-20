import cv2
import mediapipe as mp
from ultralytics import YOLO
import time
import serial

# Path to your custom YOLOv5 model
model = YOLO(r'D:\IAMTIRIEDOFTHISSHIT\yolov5\best.pt')
model.conf = 0.5

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

# Countdown for user positioning
print("Starting 8-second countdown...")
start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame.")
        break

    elapsed = int(time.time() - start_time)
    countdown = 8 - elapsed
    display_frame = frame.copy()

    # Draw hand landmarks
    rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.putText(display_frame, f"Capturing in {countdown}s...", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    cv2.imshow("Countdown + Hand Preview", display_frame)

    if countdown <= 0 or cv2.waitKey(1) & 0xFF == 27:
        break

# Capture final frame
ret, frame = cap.read()
cap.release()
cv2.destroyAllWindows()

if not ret:
    print("❌ Failed to capture final image.")
    exit()

cv2.imwrite("captured.jpg", frame)
print("📸 Image captured. Running YOLO detection...")

# YOLO prediction
results = model(frame)
detections = results[0].boxes

# Default to paper unless plastic is detected
predicted_class = "paper"
yolo_output_frame = frame.copy()

if len(detections) > 0:
    for box in detections:
        cls = int(box.cls[0].item())
        label = model.names[cls].lower()
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0].item()
        color = (255, 165, 0) if label == "plastic" else (0, 255, 0)

        cv2.rectangle(yolo_output_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(yolo_output_frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        if label == "plastic":
            predicted_class = "plastic"
            break

# Display final result
cv2.putText(yolo_output_frame, predicted_class.upper(), (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
cv2.imshow("Final Classification", yolo_output_frame)
cv2.imwrite("result.jpg", yolo_output_frame)

# ✅ Send prediction to Arduino via COM7
try:
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)  # Let Arduino reset
    ser.write((predicted_class + '\n').encode())
    print(f"✅ Sent prediction '{predicted_class}' to COM7")
    ser.close()
except Exception as e:
    print(f"❌ Serial error: {e}")

cv2.waitKey(0)
cv2.destroyAllWindows()
print("✅ Script finished.")

