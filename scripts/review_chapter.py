import sys
import subprocess
from pathlib import Path

# ---------------------------------
# CONFIG
# ---------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

SCORE_SCRIPT = SCRIPTS_DIR / "score_chapter.py"
VOICE_SCRIPT = SCRIPTS_DIR / "editorial_voice.py"

DEFAULT_TONE = "sharp_friend"

DATA_DIR = PROJECT_ROOT / "data"
EVAL_DIR = DATA_DIR / "evaluations"


# ---------------------------------
# HELPERS
# ---------------------------------

def run_command(command):
    print(f"\n▶ Running: {' '.join(command)}\n")
    result = subprocess.run(command)
    if result.returncode != 0:
        print("\n❌ Command failed. Stopping pipeline.")
        sys.exit(1)


# ---------------------------------
# MAIN
# ---------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/review_chapter.py chapter_000X.txt [tone]")
        print("Options:")
        print("  --voice-only   Skip scoring, only show editorial feedback")
        print("  --force        Re-run scoring even if evaluation exists")
        sys.exit(1)

    # ---------------------------------
    # Parse args
    # ---------------------------------

    chapter_name = None
    tone = DEFAULT_TONE
    voice_only = False
    force = False

    for arg in sys.argv[1:]:
        if arg == "--voice-only":
            voice_only = True
        elif arg == "--force":
            force = True
        elif arg.endswith(".txt"):
            chapter_name = arg
        else:
            tone = arg

    if chapter_name is None:
        print("❌ No chapter file provided.")
        sys.exit(1)

    # ---------------------------------
    # Step 1 — Scoring (Phase 3A)
    # ---------------------------------

    score_file = chapter_name.replace(".txt", "_scores.json")
    score_path = EVAL_DIR / score_file

    if voice_only:
        print("\n✓ Voice-only mode: skipping scoring.")
    else:
        if score_path.exists() and not force:
            print(f"\n✓ Using existing evaluation: {score_path}")
        else:
            if force and score_path.exists():
                print("\n⚠ Forcing re-evaluation of chapter.")
            run_command([
                sys.executable,
                str(SCORE_SCRIPT),
                chapter_name
            ])

    # ---------------------------------
    # Step 2 — Editorial Voice (Phase 3A.5)
    # ---------------------------------

    run_command([
        sys.executable,
        str(VOICE_SCRIPT),
        chapter_name,
        tone
    ])


if __name__ == "__main__":
    main()
