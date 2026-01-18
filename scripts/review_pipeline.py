# scripts/review_pipeline.py

import argparse
import os
import subprocess
import sys
from status import update_status


DATA_DIR = "data"
CHAPTER_DIR = os.path.join(DATA_DIR, "chapters")
SUMMARY_DIR = os.path.join(DATA_DIR, "summaries")
SCRIPT_DIR = "scripts"


def chapter_filename(chapter_id):
    return f"chapter_{chapter_id}.txt"


def run_script(script_name, *args):
    cmd = ["python", os.path.join(SCRIPT_DIR, script_name)] + list(args)
    print(f"[>] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        update_status(
            args[0] if args else "unknown",
            state="error",
            step=script_name,
            message=f"{script_name} failed."
        )
        sys.exit(1)


def ensure_chapter(chapter_id):
    filename = chapter_filename(chapter_id)
    path = os.path.join(CHAPTER_DIR, filename)

    if os.path.exists(path):
        print(f"[✓] Chapter exists: {filename}")
        return

    print("[+] Adding chapter")
    run_script("add_chapter.py", filename)


def ensure_summary(chapter_id):
    filename = chapter_filename(chapter_id)
    summary_file = filename.replace(".txt", "_summary.txt")
    path = os.path.join(SUMMARY_DIR, summary_file)

    if os.path.exists(path):
        print("[✓] Summary exists")
        return

    print("[+] Generating summary")
    run_script("summarize_chapter.py", filename)


def main():
    parser = argparse.ArgumentParser(description="Unified review pipeline")

    parser.add_argument("chapter_id")
    parser.add_argument("--critique", action="store_true")
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--editorial", action="store_true")
    parser.add_argument("--line-edit", choices=["paragraph", "chapter"])
    parser.add_argument(
        "--mode",
        choices=["friendly", "strict", "forensic"],
        default="friendly"
    )

    args = parser.parse_args()
    chapter_id = args.chapter_id

    update_status(
        chapter_id,
        state="running",
        step="start",
        message="Your editor is clearing his desk…"
    )

    filename = chapter_filename(chapter_id)
    summary_file = filename.replace(".txt", "_summary.txt")

    ensure_chapter(chapter_id)
    ensure_summary(chapter_id)

    update_status(
        chapter_id,
        state="running",
        step="memory",
        message="Recalling characters and unresolved tensions…"
    )
    run_script("extract_characters.py", summary_file)

    if args.critique:
        update_status(
            chapter_id,
            state="running",
            step="critique",
            message="Your editor is twirling his moustache…"
        )
        run_script("critique_chapter.py", filename, args.mode)

    if args.score:
        update_status(
            chapter_id,
            state="running",
            step="score",
            message="Assigning scores with a suspicious glare…"
        )
        run_script("score_chapter.py", filename)

    update_status(
        chapter_id,
        state="complete",
        step="done",
        message="Editorial verdict delivered."
    )

    print("\n[✓] Review pipeline complete")


if __name__ == "__main__":
    main()
