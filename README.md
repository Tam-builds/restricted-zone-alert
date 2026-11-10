# Restricted Zone Alert 🚨

A computer vision-based restricted-zone monitoring system built using Python, YOLO-World, OpenCV, and FastAPI. It detects people in video footage, checks whether they enter a predefined restricted area, captures intrusion snapshots, and displays detection results through a web dashboard.

## 🎯 Project Objective

To develop a video-based monitoring system that identifies people entering a predefined restricted zone and generates visual evidence of intrusion events.

## 🚀 Implemented Features

- YOLO object detection using Ultralytics
- YOLO-World integration for person detection
- Video frame processing using OpenCV
- Custom restricted-zone polygon definition
- Person footpoint-based zone checking
- Visual alerts using bounding-box colors
- Automatic intrusion snapshot capture
- Detection statistics and JSON report generation
- FastAPI backend with REST endpoints
- Web dashboard displaying detection metrics, processed video, and snapshots
- Browser-compatible H.264 video playback

## 🛠️ Technologies Used

- Python
- YOLO / YOLO-World
- OpenCV
- FastAPI
- Uvicorn
- FFmpeg (through imageio-ffmpeg)
- Git and GitHub

## 📁 Project Structure

```text
restricted-zone-alert/
│
├── first_detection.py
├── restricted_zone.py
├── server.py
├── requirements.txt
├── .gitignore
└── README.md
```

Generated files such as videos, snapshots, and detection reports are excluded from GitHub.

## ⚙️ Installation

Clone the repository:

```powershell
git clone https://github.com/Tam-builds/restricted-zone-alert.git
cd restricted-zone-alert
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Place your test video in the project directory using the filename expected by the detection script.

## ▶️ Running the Project

### 1. Run object detection

```powershell
python first_detection.py
```

### 2. Run restricted-zone detection

```powershell
python restricted_zone.py
```

This processes the video, checks detected people against the configured polygon, saves intrusion snapshots, and generates a detection report.

### 3. Start the FastAPI server

```powershell
python -m uvicorn server:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard
```

## 🔗 API Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | API welcome message |
| `/health` | Server health check |
| `/report` | Detection statistics and snapshot information |
| `/video` | Processed video |
| `/snapshots` | Snapshot files |
| `/dashboard` | Monitoring dashboard |

**Note:** The dashboard requires the generated detection report, snapshots, and browser-compatible processed video. These are generated locally and are not included in the repository.

## 🧠 Key Learning Outcomes

- Understanding object detection using YOLO
- Working with video frames using OpenCV
- Understanding bounding boxes and confidence scores
- Applying polygon-based spatial logic
- Building a REST API using FastAPI
- Connecting a backend to a web dashboard
- Managing project dependencies and version control using Git

## 🔮 Future Improvements

- Live webcam or CCTV stream processing
- Real-time notifications through email or messaging services
- Entry/exit event tracking
- Database integration for storing intrusion history
- Improved detection accuracy and performance
- Optional AI-based verification of detected events

## 👩‍💻 Author

Tam-builds

GitHub: https://github.com/Tam-builds

---

**Project status:** Core video-based restricted-zone detection and dashboard implementation completed. Further enhancements are planned.