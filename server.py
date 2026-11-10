
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

app = FastAPI(
    title="Restricted Zone Alert API",
    description="Backend for the Restricted Zone Detection System",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
REPORT_PATH = BASE_DIR / "detection_report.json"
VIDEO_PATH = BASE_DIR / "restricted_zone_browser.mp4"
SNAPSHOT_FOLDER = BASE_DIR / "snapshots"

SNAPSHOT_FOLDER.mkdir(exist_ok=True)

# Serve snapshot images
app.mount(
    "/snapshots",
    StaticFiles(directory=SNAPSHOT_FOLDER),
    name="snapshots"
)


@app.get("/")
def home():
    return {
        "message": "Restricted Zone Alert API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/report")
def detection_report():

    if not REPORT_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Detection report not found. Run restricted_zone.py first."
        )

    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        report = json.load(file)

    snapshots = sorted(
        file.name for file in SNAPSHOT_FOLDER.glob("*.jpg")
    )

    report["snapshot_files"] = snapshots
    report["video_generated"] = VIDEO_PATH.exists()

    return report



@app.get("/video")
def get_video():

    if not VIDEO_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Output video not found."
        )

    return FileResponse(
        path=VIDEO_PATH,
        media_type="video/mp4",
        content_disposition_type="inline"
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Restricted Zone Alert Dashboard</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                margin: 0;
                padding: 30px;
                color: #1e293b;
            }

            h1 {
                color: #0f172a;
            }

            .subtitle {
                color: #64748b;
            }

            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
                margin: 25px 0;
            }

            .card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px #00000010;
            }

            .card h3 {
                color: #64748b;
                font-size: 14px;
            }

            .number {
                font-size: 28px;
                font-weight: bold;
            }

            .snapshots {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
            }

            .snapshot {
                background: white;
                padding: 10px;
                border-radius: 10px;
            }

            .snapshot img {
                width: 100%;
                border-radius: 6px;
            }

            video {
                width: 100%;
                max-width: 800px;
                border-radius: 10px;
                background: black;
            }
        </style>
    </head>

    <body>

        <h1>Restricted Zone Alert</h1>
        <p class="subtitle">
            Vision AI Monitoring Dashboard
        </p>

        <h2>Detection Summary</h2>

        <div class="stats">
            <div class="card">
                <h3>Frames Processed</h3>
                <div class="number" id="frames">Loading...</div>
            </div>

            <div class="card">
                <h3>Intrusion Detections</h3>
                <div class="number" id="detections">Loading...</div>
            </div>

            <div class="card">
                <h3>Frames with Intrusion</h3>
                <div class="number" id="intrusionFrames">Loading...</div>
            </div>

            <div class="card">
                <h3>Snapshots This Run</h3>
                <div class="number" id="snapshots">Loading...</div>
            </div>
        </div>

        <h2>Processed Video</h2>

        <video controls>
            <source src="/video" type="video/mp4">
            Your browser does not support video playback.
        </video>

        <h2>Intrusion Snapshots</h2>

        <div class="snapshots" id="snapshotGallery">
            Loading snapshots...
        </div>

        <script>
            async function loadDashboard() {

                try {
                    const response = await fetch("/report");

                    if (!response.ok) {
                        throw new Error("Could not load report");
                    }

                    const data = await response.json();

                    document.getElementById("frames").textContent =
                        data.total_frames_processed;

                    document.getElementById("detections").textContent =
                        data.total_intrusion_detections;

                    document.getElementById("intrusionFrames").textContent =
                        data.frames_containing_intrusion;

                    document.getElementById("snapshots").textContent =
                        data.snapshots_saved_this_run;

                    const gallery =
                        document.getElementById("snapshotGallery");

                    gallery.innerHTML = "";

                    data.snapshot_files.forEach(filename => {

                        const card = document.createElement("div");
                        card.className = "snapshot";

                        const img = document.createElement("img");
                        img.src = "/snapshots/" + encodeURIComponent(filename);
                        img.alt = "Intrusion snapshot";

                        const caption = document.createElement("p");
                        caption.textContent = filename;

                        card.appendChild(img);
                        card.appendChild(caption);

                        gallery.appendChild(card);
                    });

                } catch (error) {
                    document.getElementById("snapshotGallery").textContent =
                        "Error loading dashboard: " + error.message;
                }
            }

            loadDashboard();
        </script>

    </body>
    </html>
    """
