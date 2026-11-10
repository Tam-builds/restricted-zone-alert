# Restricted Zone Alert 🚨

A computer vision project built using Python, YOLO and OpenCV to detect objects in video footage. The project is being developed into a real-time restricted-zone monitoring system that can identify unauthorized entry and generate alerts.

## 🎯 Project Objective

The goal is to build a system that monitors a video feed, detects people, identifies when they enter a predefined restricted area, and captures evidence for security monitoring.

## 🚀 Current Progress

- [x] Python environment setup
- [x] YOLO object detection setup
- [x] Video-based object detection
- [x] Bounding box and confidence score visualization
- [x] Detection output video generation
- [ ] YOLO-World integration
- [ ] Restricted-zone polygon detection
- [ ] Automatic intrusion snapshots
- [ ] FastAPI backend
- [ ] Web dashboard

## 🛠️ Technologies Used

- Python
- YOLO (Ultralytics)
- OpenCV
- FastAPI
- Git and GitHub

## 📁 Project Structure

```text
restricted-zone-alert/
│
├── first_detection.py
├── requirements.txt
├── .gitignore
└── README.md
```

Additional files and modules will be added as development progresses.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Tam-builds/restricted-zone-alert.git
cd restricted-zone-alert
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

Place your own test video in the project folder and name it `video1.mp4`.

Run:

```bash
python first_detection.py
```

The YOLO model detects objects and saves an annotated output video in the generated `runs/detect/` directory.

## 🧠 Learning Outcomes

- Understanding object detection using YOLO.
- Working with video frames using OpenCV.
- Understanding bounding boxes, class labels and confidence scores.
- Building a foundation for real-time computer vision applications.

## 🔮 Future Scope

- Detect people using YOLO-World.
- Define restricted areas using polygon coordinates.
- Generate alerts when people enter restricted areas.
- Capture snapshots of intrusion events.
- Build a FastAPI backend and monitoring dashboard.

## 👩‍💻 Author

**Tam-builds**

GitHub: https://github.com/Tam-builds

---

*This project is currently under development.*
