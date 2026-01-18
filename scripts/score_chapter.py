from pathlib import Path
import json
import sys
from openai import OpenAI, RateLimitError

# ---------------------------------
# CONFIG
# ---------------------------------

DATA_DIR = Path("data")
CHAPTERS_DIR = DATA_DIR / "chapters"
SUMMARIES_DIR = DATA_DIR / "summaries"
CHARACTERS_DIR = DATA_DIR / "characters"
EVAL_DIR = DATA_DIR / "evaluations"

EVAL_DIR.mkdir(exist_ok=True)

DIMENSIONS = [
    "prose_quality",
    "pacing",
    "character_consistency",
    "character_depth",
    "emotional_impact",
    "dialogue_quality",
    "plot_logic",
    "thematic_coherence"
]

MODEL = "gpt-4.1-mini"

client = OpenAI()

# ---------------------------------
# LOADERS
# ---------------------------------

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_chapter(name):
    path = CHAPTERS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Chapter not found: {path}")
    return load_text(path)


def load_summaries():
    blocks = []
    if not SUMMARIES_DIR.exists():
        return ""
    for f in sorted(SUMMARIES_DIR.glob("*_summary.txt")):
        blocks.append(f"--- {f.name} ---\n{load_text(f)}")
    return "\n\n".join(blocks)


def load_characters():
    blocks = []
    if not CHARACTERS_DIR.exists():
        return ""
    for f in sorted(CHARACTERS_DIR.glob("*.json")):
        data = json.loads(load_text(f))
        blocks.append(f"--- {f.stem} ---\n{json.dumps(data, indent=2)}")
    return "\n\n".join(blocks)


# ---------------------------------
# PROMPT
# ---------------------------------

def build_prompt(chapter_text, summaries, characters):
    return f"""
You are a professional fiction editor.

Your task is to evaluate ONE chapter of a novel using serious editorial judgment.
This is NOT a rules-based task.

Requirements:
- Score honestly (0–100 or null)
- Explain reasoning clearly
- Cite evidence explicitly
- Admit uncertainty
- Do NOT invent canon
- If something cannot yet be judged, say so

--------------------------------
PAST CHAPTER SUMMARIES
--------------------------------
{summaries or "[No summaries available]"}

--------------------------------
CHARACTER MEMORY
--------------------------------
{characters or "[No character memory available]"}

--------------------------------
CURRENT CHAPTER
--------------------------------
{chapter_text}

--------------------------------
OUTPUT FORMAT (STRICT JSON)
--------------------------------

For EACH dimension below, return an object with:
- score (0–100 or null)
- justification (array of strings)
- evidence (array of explicit references)
- confidence ("high" | "medium" | "low")
- notes (string, optional)

Dimensions:
{DIMENSIONS}
"""


# ---------------------------------
# AI CALL
# ---------------------------------

def run_editorial_scoring(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a careful, conservative literary editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    return json.loads(content)


# ---------------------------------
# MAIN
# ---------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/score_chapter.py chapter_000X.txt")
        sys.exit(1)

    chapter_name = sys.argv[1]
    out_name = chapter_name.replace(".txt", "_scores.json")
    out_path = EVAL_DIR / out_name

    chapter_text = load_chapter(chapter_name)
    summaries = load_summaries()
    characters = load_characters()

    prompt = build_prompt(chapter_text, summaries, characters)

    try:
        report = run_editorial_scoring(prompt)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"[OK] Editorial evaluation saved to {out_path}")

    except RateLimitError:
        print("⚠️ OpenAI rate limit hit during scoring.")

        if out_path.exists():
            print(f"[✓] Existing score reused: {out_path}")
        else:
            print("[!] No existing score available. Scoring skipped.")

    except Exception as e:
        print("❌ Scoring failed:", str(e))


if __name__ == "__main__":
    main()
