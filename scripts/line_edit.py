import sys
from pathlib import Path
from openai import OpenAI
from config import MOCK_MODE

# ---------------------------------
# CONFIG
# ---------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHAPTER_DIR = DATA_DIR / "chapters"
LINE_EDIT_DIR = DATA_DIR / "line_edits"

MODEL = "gpt-4.1-mini"
client = OpenAI()

# ---------------------------------
# LOADERS
# ---------------------------------

def load_chapter(chapter_name):
    path = CHAPTER_DIR / chapter_name
    if not path.exists():
        raise FileNotFoundError(f"Chapter not found: {path}")
    return path.read_text(encoding="utf-8")


def split_paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]

# ---------------------------------
# PROMPT
# ---------------------------------

def build_prompt(text):
    return f"""
You are a senior fiction editor performing a **light line edit**.

STRICT RULES:
- Preserve the author's voice and rhythm
- Fix grammar, clarity, and awkward phrasing only
- Do NOT add new content
- Do NOT change meaning
- Do NOT alter imagery or metaphors unless broken
- Keep edits minimal and local

TASK:
1. Present the ORIGINAL text
2. Present a LIGHTLY EDITED version
3. Briefly explain what was improved and why

TEXT TO EDIT:
{text}

OUTPUT FORMAT (MANDATORY):
ORIGINAL:
<original text>

EDITED:
<edited text>

WHY:
<short explanation>
"""

# ---------------------------------
# CORE LOGIC
# ---------------------------------

def run_line_edit(text, output_path):
    # ---------- MOCK MODE ----------
    if MOCK_MODE:
        if not output_path.exists():
            print("\n❌ MOCK MODE: No saved line edit found.")
            print(f"Expected: {output_path}")
            print("Run once with MOCK_MODE = False to generate it.\n")
            sys.exit(1)

        return output_path.read_text(encoding="utf-8")

    # ---------- LIVE MODE ----------
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful fiction editor who values restraint "
                    "and clarity over clever rewriting."
                )
            },
            {
                "role": "user",
                "content": build_prompt(text)
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    LINE_EDIT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")

    return result

# ---------------------------------
# CLI
# ---------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/line_edit.py chapter_000X.txt")
        print("  python scripts/line_edit.py chapter_000X.txt --paragraph N")
        sys.exit(1)

    chapter_name = sys.argv[1]
    paragraph_index = None

    if "--paragraph" in sys.argv:
        idx = sys.argv.index("--paragraph")
        paragraph_index = int(sys.argv[idx + 1])

    chapter_text = load_chapter(chapter_name)
    paragraphs = split_paragraphs(chapter_text)

    if paragraph_index is not None:
        if paragraph_index < 0 or paragraph_index >= len(paragraphs):
            print("Invalid paragraph index.")
            sys.exit(1)

        text_to_edit = paragraphs[paragraph_index]
        output_path = LINE_EDIT_DIR / f"{chapter_name}_para_{paragraph_index}_line_edit.txt"
    else:
        text_to_edit = chapter_text
        output_path = LINE_EDIT_DIR / f"{chapter_name}_line_edit.txt"

    result = run_line_edit(text_to_edit, output_path)

    print("\n" + "=" * 72 + "\n")
    print(result)
    print("\n" + "=" * 72 + "\n")

# ---------------------------------
# ENTRY
# ---------------------------------

if __name__ == "__main__":
    main()
