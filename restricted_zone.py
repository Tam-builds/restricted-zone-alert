
import cv2
import numpy as np
import json
from pathlib import Path
from ultralytics import YOLOWorld

# PROJECT PATHS
BASE_DIR = Path(__file__).resolve().parent

video_path = BASE_DIR / "video1.mp4"
output_path = BASE_DIR / "restricted_zone_output.mp4"
snapshot_folder = BASE_DIR / "snapshots"
report_path = BASE_DIR / "detection_report.json"

# LOAD MODEL
print("Loading YOLO-World model...", flush=True)

model = YOLOWorld("yolov8s-worldv2.pt")
model.set_classes(["person"])

print("YOLO-World is ready!", flush=True)

# OPEN INPUT VIDEO
cap = cv2.VideoCapture(str(video_path))

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

# DEFINE RESTRICTED ZONE
restricted_zone = [
    (1550, 300),
    (1910, 300),
    (1910, 1080),
    (1550, 1080)
]

zone_contour = np.array(
    restricted_zone, dtype=np.int32
).reshape((-1, 1, 2))

# CREATE OUTPUT VIDEO
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (width, height)
)

if not writer.isOpened():
    raise RuntimeError("Could not create output video!")

# CREATE SNAPSHOT FOLDER
snapshot_folder.mkdir(exist_ok=True)

# INITIALIZE COUNTERS
frame_count = 0
intrusion_detections = 0
intrusion_frames = 0
snapshots_saved = 0

# SNAPSHOT COOLDOWN
cooldown = 3.0
last_snapshot_time = -cooldown

print("\nStarting restricted zone detection...\n", flush=True)

# PROCESS VIDEO FRAME BY FRAME
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1
    video_time = frame_count / fps

    results = model.predict(
        frame,
        conf=0.25,
        verbose=False
    )

    # DRAW RESTRICTED ZONE
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
        (
            restricted_zone[0][0],
            max(restricted_zone[0][1] - 15, 25)
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    intrusion_in_current_frame = False

    # PROCESS DETECTIONS
    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].cpu().tolist()
            )

            # BOTTOM-CENTRE POINT OF BOUNDING BOX
            foot_x = (x1 + x2) // 2
            foot_y = y2

            foot_point = (foot_x, foot_y)

            # CHECK WHETHER PERSON IS INSIDE POLYGON
            position = cv2.pointPolygonTest(
                zone_contour,
                (float(foot_x), float(foot_y)),
                False
            )

            if position >= 0:

                color = (0, 0, 255)
                label = "INTRUSION"

                intrusion_detections += 1
                intrusion_in_current_frame = True

            else:

                color = (0, 255, 0)
                label = "PERSON"

            # DRAW BOUNDING BOX
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # DRAW FOOTPOINT
            cv2.circle(
                frame,
                foot_point,
                6,
                (255, 0, 0),
                -1
            )

            # DRAW LABEL
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    # HANDLE INTRUSION ALERT
    if intrusion_in_current_frame:

        intrusion_frames += 1

        if video_time - last_snapshot_time >= cooldown:

            snapshot_path = (
                snapshot_folder /
                f"intrusion_{frame_count}.jpg"
            )

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

    # WRITE FRAME TO OUTPUT VIDEO
    writer.write(frame)

    if frame_count % 50 == 0:
        print(
            f"Processing frame {frame_count}...",
            flush=True
        )

# RELEASE RESOURCES
cap.release()
writer.release()
cv2.destroyAllWindows()

# COUNT ALL SNAPSHOTS IN THE FOLDER
total_snapshot_files = len(
    list(snapshot_folder.glob("*.jpg"))
)

# CREATE DETECTION REPORT
report = {
    "project": "Restricted Zone Alert",
    "video_generated": output_path.exists(),
    "total_frames_processed": frame_count,
    "total_intrusion_detections": intrusion_detections,
    "frames_containing_intrusion": intrusion_frames,
    "snapshots_saved_this_run": snapshots_saved,
    "total_snapshots_in_folder": total_snapshot_files,
    "output_video": output_path.name
}

# SAVE REPORT AS JSON
with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

# DISPLAY FINAL REPORT
print("\n========== DETECTION REPORT ==========")

for key, value in report.items():
    print(f"{key}: {value}")

print("\nReport saved to:", report_path)
print("\nRestricted zone detection completed!")
