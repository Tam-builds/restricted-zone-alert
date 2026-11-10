
from ultralytics import YOLO
from collections import Counter

# Load YOLO model
model = YOLO("yolov8n.pt")

# Store detection statistics
total_frames = 0
total_detections = 0
class_counts = Counter()

# Process video one frame at a time
results = model.predict(
    source="video1.mp4",
    save=True,
    stream=True,
    conf=0.25
)

for result in results:
    total_frames += 1

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        total_detections += 1
        class_counts[class_name] += 1

# Display final report
print("\n--- YOLO DETECTION REPORT ---")
print("Total frames:", total_frames)
print("Total detections:", total_detections)
print("Detected objects:")

for name, count in class_counts.items():
    print(name, ":", count)

print("\nDetection completed!")
