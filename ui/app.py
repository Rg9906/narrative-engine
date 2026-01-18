from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import os
import json

# ---------- PATH SETUP ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CHAPTERS_DIR = os.path.join(DATA_DIR, "chapters")
STATUS_DIR = os.path.join(DATA_DIR, "status")

# ---------- APP ----------

app = FastAPI(title="Narrative Memory Engine UI")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ---------- HELPERS ----------

def list_chapters():
    if not os.path.exists(CHAPTERS_DIR):
        return []
    files = sorted(f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".txt"))
    return [f.replace("chapter_", "").replace(".txt", "") for f in files]


def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def read_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ---------- ROUTES ----------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "chapters": list_chapters()
        }
    )


@app.post("/add", response_class=HTMLResponse)
def add_chapter(
    request: Request,
    chapter_id: str = Form(...),
    chapter_text: str = Form(...)
):
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    path = os.path.join(CHAPTERS_DIR, f"chapter_{chapter_id}.txt")

    if os.path.exists(path):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "chapters": list_chapters(),
                "error": f"Chapter {chapter_id} already exists."
            }
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(chapter_text.strip())

    return RedirectResponse("/", status_code=303)


@app.get("/chapter/{chapter_id}", response_class=HTMLResponse)
def chapter_detail(request: Request, chapter_id: str):
    context = {
        "request": request,
        "chapter_id": chapter_id,
        "chapter": read_file(
            os.path.join(CHAPTERS_DIR, f"chapter_{chapter_id}.txt")
        ),
        "summary": read_file(
            os.path.join(DATA_DIR, "summaries", f"chapter_{chapter_id}_summary.txt")
        ),
        "critique": read_file(
            os.path.join(DATA_DIR, "evaluations", f"chapter_{chapter_id}_critique.txt")
        ),
        "score": read_json(
            os.path.join(DATA_DIR, "evaluations", f"chapter_{chapter_id}_scores.json")
        ),
    }

    return templates.TemplateResponse("chapter.html", context)


@app.post("/run/{chapter_id}")
def run_pipeline(
    chapter_id: str,
    mode: str = Form("friendly")
):
    cmd = [
        "python",
        os.path.join(SCRIPTS_DIR, "review_pipeline.py"),
        chapter_id,
        "--critique",
        "--score",
        f"--mode={mode}"
    ]

    subprocess.Popen(cmd, cwd=PROJECT_ROOT)

    # 🔴 NO REDIRECT — THIS IS THE KEY FIX
    return JSONResponse({"status": "started"})


# ---------- STATUS API ----------

@app.get("/status/{chapter_id}")
def get_status(chapter_id: str):
    path = os.path.join(STATUS_DIR, f"chapter_{chapter_id}.json")
    if not os.path.exists(path):
        return JSONResponse({})
    return JSONResponse(json.load(open(path)))
