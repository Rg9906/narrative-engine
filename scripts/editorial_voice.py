from pathlib import Path
import json
import sys
from openai import OpenAI
from config import MOCK_MODE

# ---------------------------------
# CONFIG
# ---------------------------------

DATA_DIR = Path("data")
EVAL_DIR = DATA_DIR / "evaluations"
MOCK_DIR = DATA_DIR / "mock_outputs"

MODEL = "gpt-4.1-mini"
client = OpenAI()


TONE_PROFILES = {
    "workshop_partner": {
        "warmth": "high",
        "directness": "medium",
        "playfulness": "medium",
        "pedagogy": "high",
        "wit": "light"
    },
    "sharp_friend": {
        "warmth": "high",
        "directness": "high",
        "playfulness": "high",
        "pedagogy": "medium",
        "wit": "sharp"
    },
    "senior_editor": {
        "warmth": "medium",
        "directness": "high",
        "playfulness": "low",
        "pedagogy": "medium",
        "wit": "dry"
    },
    "professor": {
        "warmth": "low",
        "directness": "medium",
        "playfulness": "low",
        "pedagogy": "high",
        "wit": "minimal"
    }
}

DEFAULT_TONE = "sharp_friend"

# ---------------------------------
# LOADERS
# ---------------------------------

def load_scores(chapter_name: str):
    score_file = chapter_name.replace(".txt", "_scores.json")
    path = EVAL_DIR / score_file

    if not path.exists():
        raise FileNotFoundError(f"Score file not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))

# ---------------------------------
# PROMPT
# ---------------------------------

def build_prompt(scores, tone_name):
    tone = TONE_PROFILES.get(tone_name, TONE_PROFILES[DEFAULT_TONE])

    return f"""
You are a human fiction editor speaking directly to the author.

EDITORIAL STANCE:
- Warmth: {tone['warmth']}
- Directness: {tone['directness']}
- Playfulness: {tone['playfulness']}
- Pedagogy (teaching): {tone['pedagogy']}
- Wit: {tone['wit']}

IMPORTANT GUIDANCE:
- Wit should be intelligent and restrained — dry observations, gentle irony, sharp clarity.
- Do NOT be goofy, meme-y, or flippant.
- Think: an editor who respects the work and the writer.

CRITICAL STRUCTURE (DO NOT IGNORE THIS):
You MUST spend meaningful time on:
1. What the chapter is doing WELL (strengths)
2. What needs improvement (fixes)

The strengths section is NOT optional.
It should feel sincere, specific, and craft-focused.

TASK:
Using the structured evaluation below as your ONLY source of truth,
talk to the author like a real editor sitting across the table.

WHAT TO DO:
- Start with strengths: identify 2–3 things that genuinely work
- Explain WHY those things work
- Signal what the author should continue doing
- Then transition to issues and opportunities for improvement
- For at least ONE issue, show a short example of how it could be revised
  (1–2 lines max; do not rewrite entire paragraphs)
- Be honest but humane
- If something is early-stage or uncertain, say so plainly

STRICT RULES:
- Do NOT invent new critiques
- Do NOT contradict the evaluation
- Do NOT resolve ambiguities
- Do NOT change canon
- Do NOT summarize the JSON — interpret it

STRUCTURED EVALUATION (SOURCE OF TRUTH):
{json.dumps(scores, indent=2)}

OUTPUT FORMAT:
Plain text.
Address the author directly.
Use natural paragraph breaks.
No JSON.
No bullet lists unless they feel conversational.
"""

# ---------------------------------
# AI CALL
# ---------------------------------

def generate_editorial_voice(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced fiction editor who believes good critique "
                    "should leave the writer clearer and more motivated than before."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.65
    )

    return response.choices[0].message.content

# ---------------------------------
# MAIN
# ---------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/editorial_voice.py chapter_000X.txt [tone]")
        print("Available tones:", ", ".join(TONE_PROFILES.keys()))
        sys.exit(1)

    chapter_name = sys.argv[1]
    tone = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_TONE

    scores = load_scores(chapter_name)
    prompt = build_prompt(scores, tone)

    # ---------- MOCK MODE ----------
    if MOCK_MODE:
        mock_path = MOCK_DIR / f"{chapter_name}_voice.txt"
        if not mock_path.exists():
            print("\n❌ MOCK MODE: No mock editorial output found.")
            print(f"Expected: {mock_path}")
            print("Run once with MOCK_MODE = False to generate it.\n")
            sys.exit(1)

        print("\n" + "=" * 72 + "\n")
        print(mock_path.read_text(encoding="utf-8"))
        print("\n" + "=" * 72 + "\n")
        return

    # ---------- LIVE MODE ----------
    feedback = generate_editorial_voice(prompt)

    print("\n" + "=" * 72 + "\n")
    print(feedback)
    print("\n" + "=" * 72 + "\n")

    # Save for demo reuse
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    (MOCK_DIR / f"{chapter_name}_voice.txt").write_text(
        feedback, encoding="utf-8"
    )

if __name__ == "__main__":
    main()
