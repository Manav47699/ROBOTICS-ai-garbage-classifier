import cv2
import mediapipe as mp
from ultralytics import YOLO
import time

# ✅ Load YOLOv5 model
# IMPORTANT: Ensure the path to your best.pt model is correct.
# This model is specific to the user's local file system.
model = YOLO(r'D:\IAMTIRIEDOFTHISSHIT\yolov5\best.pt')
model.conf = 0.5 # Set confidence threshold for YOLO detections

# ✅ Mediapipe hands initialization (tracking mode enabled)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,  # Set to False for live video stream tracking
    max_num_hands=2,          # Detect up to two hands
    min_detection_confidence=0.5 # Minimum confidence for hand detection
)
mp_drawing = mp.solutions.drawing_utils # Utility for drawing landmarks

# ✅ Open webcam
cap = cv2.VideoCapture(0) # 0 refers to the default webcam

# Check if webcam was opened successfully
if not cap.isOpened():
    print("❌ Error: Could not open webcam. Please ensure it's connected and not in use.")
    exit()

# ✅ 8-second countdown with live Mediapipe hand visualization
print("Starting 8-second countdown...")
start_time = time.time()
while True:
    ret, frame = cap.read() # Read a frame from the webcam
    if not ret:
        print("❌ Failed to access webcam during countdown. Exiting.")
        break # Exit loop if frame cannot be read

    elapsed = int(time.time() - start_time)
    countdown = 8 - elapsed # Countdown from 8 seconds
    display_frame = frame.copy() # Create a copy to draw on for display

    # ✅ Hand detection during countdown (for live preview)
    rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB) # Convert BGR to RGB for Mediapipe
    hand_results = hands.process(rgb_frame) # Process the frame for hand landmarks

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Draw hand landmarks and connections on the display frame
            mp_drawing.draw_landmarks(display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ✅ Countdown display on the frame
    cv2.putText(display_frame, f"Capturing in {countdown}s...", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3) # Red text for countdown
    cv2.imshow("Countdown + Hand Preview", display_frame) # Show the preview window

    if countdown <= 0:
        print("Countdown finished. Capturing image.")
        break # Exit loop when countdown reaches zero

    # Check for 'Esc' key press to exit early
    if cv2.waitKey(1) & 0xFF == 27: # 27 is the ASCII code for the 'Esc' key
        print("Exiting countdown early.")
        cap.release()
        cv2.destroyAllWindows()
        exit() # Exit the script

# ✅ Capture final image after countdown
ret, frame = cap.read() # Read the final frame
cap.release() # Release the webcam resource
cv2.destroyAllWindows() # Close all OpenCV windows

if not ret:
    print("❌ Failed to capture final image. Exiting.")
    exit()

cv2.imwrite("captured.jpg", frame) # Save the captured image

# ✅ YOLO detection on the captured image
print("Running YOLO detection...")
results = model(frame) # Perform detection
detections = results[0].boxes # Get bounding box detections

# Flags to control which result (YOLO or Mediapipe) to display
display_yolo_result = False
display_mediapipe_result = False

# Create a copy of the frame to draw YOLO detections on, preserving the original for Mediapipe if needed
yolo_output_frame = frame.copy()

if len(detections) > 0:
    # First, check if 'plastic' is among the detections
    plastic_detected = False
    for box in detections:
        cls = int(box.cls[0].item())
        label = model.names[cls]
        if label == "plastic":
            plastic_detected = True
            break # Found plastic, prioritize YOLO output for plastic

    if plastic_detected:
        print("YOLO detected 'plastic'. Displaying YOLO results.")
        display_yolo_result = True
        # Draw all YOLO detections on yolo_output_frame
        for box in detections:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = model.names[cls]

            color = (0, 255, 0) # Default green for general detections
            if label == "plastic":
                color = (255, 165, 0) # Orange color for 'plastic' to highlight it

            cv2.rectangle(yolo_output_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(yolo_output_frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    else:
        # If no 'plastic' was detected by YOLO, now check if 'paper' was detected.
        paper_detected_by_yolo = False
        for box in detections:
            cls = int(box.cls[0].item())
            label = model.names[cls]
            if label == "paper":
                paper_detected_by_yolo = True
                break # Found 'paper', force Mediapipe as per request

        if paper_detected_by_yolo:
            # If 'paper' is detected by YOLO, force Mediapipe logic
            print("YOLO detected 'paper'. Falling back to Mediapipe for 'paper' detection.")
            display_mediapipe_result = True
        else:
            # YOLO detected something else (not 'plastic', not 'paper'), display those YOLO results
            print("YOLO detected other objects. Displaying YOLO results.")
            display_yolo_result = True
            for box in detections:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = model.names[cls]
                cv2.rectangle(yolo_output_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(yolo_output_frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
else:
    # ❌ No YOLO detections at all, use Mediapipe fallback
    print("No YOLO detections. Falling back to Mediapipe.")
    display_mediapipe_result = True

# Prepare the final frame to be displayed based on the flags
final_display_frame = frame.copy() # Start with a clean copy of the original frame

if display_yolo_result:
    final_display_frame = yolo_output_frame # If YOLO result is chosen, use the frame with YOLO drawings
elif display_mediapipe_result:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert original frame to RGB for Mediapipe
    hand_results = hands.process(rgb_frame) # Process for hand landmarks

    hand_count = 0
    if hand_results.multi_hand_landmarks:
        hand_count = len(hand_results.multi_hand_landmarks)
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Draw hand landmarks and connections on the final display frame
            mp_drawing.draw_landmarks(final_display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Determine label based on hand count
    if hand_count == 1:
        label = "Paper (One hand detected)"
    elif hand_count == 2:
        label = "Unknown (Two hands detected)"
    else:
        label = "Nothing detected"

    # Put text on the final display frame for Mediapipe results
    cv2.putText(final_display_frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 0, 0), 3) # Blue text for Mediapipe results
else:
    # This case should theoretically not be reached if all conditions are covered.
    # It acts as a safeguard.
    cv2.putText(final_display_frame, "No specific detection criteria met", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255), 3) # Red text for error/unhandled case

# ✅ Show and save the final result
print("Displaying final result. Press any key to close.")
cv2.imshow("Final Result", final_display_frame) # Show the final result window
cv2.imwrite("result.jpg", final_display_frame) # Save the final result image
cv2.waitKey(0) # Wait indefinitely until a key is pressed
cv2.destroyAllWindows() # Close all OpenCV windows
print("Script finished.")
