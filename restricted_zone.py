
import cv2
import numpy as np
import time
from pathlib import Path
from ultralytics import YOLOWorld


# ==========================================
# 1. LOAD YOLO-WORLD MODEL
# ==========================================

print("Loading YOLO-World model...", flush=True)

model = YOLOWorld("yolov8s-worldv2.pt")

# Detect only people
model.set_classes(["person"])

print("YOLO-World is ready!", flush=True)


# ==========================================
# 2. OPEN INPUT VIDEO
# ==========================================

video_path = "video1.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("Could not open input video!")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

print("Video width:", width)
print("Video height:", height)
print("Video FPS:", fps)


# ==========================================
# 3. DEFINE RESTRICTED ZONE
# ==========================================

restricted_zone = [
    (1550, 300),
    (1910, 300),
    (1910, 1080),
    (1550, 1080)
]

# Convert polygon into OpenCV contour format
zone_contour = np.array(
    restricted_zone,
    dtype=np.int32
).reshape((-1, 1, 2))


# ==========================================
# 4. CREATE OUTPUT VIDEO
# ==========================================

output_path = "restricted_zone_output.mp4"

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    output_path,
    fourcc,
    fps,
    (width, height)
)

if not writer.isOpened():
    raise RuntimeError("Could not create output video!")


# ==========================================
# 5. CREATE SNAPSHOT FOLDER
# ==========================================

snapshot_folder = Path("snapshots")

snapshot_folder.mkdir(exist_ok=True)


# ==========================================
# 6. INITIALIZE COUNTERS
# ==========================================

frame_count = 0

# Total person detections inside restricted zone
intrusion_detections = 0

# Number of frames containing at least one intrusion
intrusion_frames = 0

# Number of snapshots saved
snapshots_saved = 0

# Snapshot cooldown in seconds
cooldown = 3.0

# Allows the first intrusion to save a snapshot
last_snapshot_time = -cooldown


# ==========================================
# 7. PROCESS VIDEO FRAME BY FRAME
# ==========================================

print("\nStarting restricted zone detection...\n", flush=True)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # Video timestamp in seconds
    video_time = frame_count / fps

    # Detect people in the current frame
    results = model.predict(
        frame,
        conf=0.25,
        verbose=False
    )

    # Draw restricted zone
    cv2.polylines(
        frame,
        [zone_contour],
        True,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (restricted_zone[0][0], max(restricted_zone[0][1] - 15, 25)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    # Track whether this frame contains an intrusion
    intrusion_in_current_frame = False

    # Process detections
    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            # Get bounding box coordinates
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].cpu().tolist()
            )

            # Calculate bottom-centre point
            foot_x = (x1 + x2) // 2
            foot_y = y2

            foot_point = (foot_x, foot_y)

            # Check whether the point is inside the polygon
            position = cv2.pointPolygonTest(
                zone_contour,
                (float(foot_x), float(foot_y)),
                False
            )

            if position >= 0:

                # Person is inside restricted zone
                color = (0, 0, 255)
                label = "INTRUSION"

                intrusion_detections += 1
                intrusion_in_current_frame = True

            else:

                # Person is outside restricted zone
                color = (0, 255, 0)
                label = "PERSON"

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Draw foot point
            cv2.circle(
                frame,
                foot_point,
                6,
                (255, 0, 0),
                -1
            )

            # Draw detection label
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    # ======================================
    # 8. HANDLE INTRUSION ALERTS
    # ======================================

    if intrusion_in_current_frame:

        intrusion_frames += 1

        # Check 3-second cooldown
        if video_time - last_snapshot_time >= cooldown:

            snapshot_path = (
                snapshot_folder /
                f"intrusion_{frame_count}.jpg"
            )

            # Save annotated frame
            saved = cv2.imwrite(
                str(snapshot_path),
                frame
            )

            if saved:
                snapshots_saved += 1
                last_snapshot_time = video_time

                print(
                    f"ALERT! Snapshot saved: {snapshot_path}",
                    flush=True
                )

    # Save annotated frame to output video
    writer.write(frame)

    # Display progress every 50 frames
    if frame_count % 50 == 0:
        print(
            f"Processing frame {frame_count}...",
            flush=True
        )


# ==========================================
# 9. RELEASE VIDEO RESOURCES
# ==========================================

cap.release()
writer.release()

cv2.destroyAllWindows()


# ==========================================
# 10. FINAL REPORT
# ==========================================

print("\n========== DETECTION REPORT ==========")

print("Frames processed:", frame_count)

print("Intrusion detections:", intrusion_detections)

print("Frames containing intrusion:", intrusion_frames)

print("Snapshots saved:", snapshots_saved)

print("Output video:", output_path)

print("Snapshot folder:", snapshot_folder)

print("\nRestricted zone detection completed!")
