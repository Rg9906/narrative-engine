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
SUMMARY_DIR = DATA_DIR / "summaries"
CHAR_DIR = DATA_DIR / "characters"

MODEL = "gpt-4.1-mini"
client = OpenAI()

MAX_CONTEXT_CHARS = 6000  # hard safety cap


# ---------------------------------
# LOADERS
# ---------------------------------

def load_chapter(chapter_name):
    path = CHAPTER_DIR / chapter_name
    if not path.exists():
        raise FileNotFoundError(f"Chapter not found: {path}")
    return path.read_text(encoding="utf-8")


def load_summaries():
    summaries = []
    for f in sorted(SUMMARY_DIR.glob("*_summary.txt")):
        summaries.append(f.read_text(encoding="utf-8"))
    return "\n\n".join(summaries)


def load_characters():
    chars = []
    for f in sorted(CHAR_DIR.glob("*.json")):
        chars.append(f.read_text(encoding="utf-8"))
    return "\n\n".join(chars)


def trim(text, limit):
    return text[-limit:] if len(text) > limit else text


# ---------------------------------
# PROMPT
# ---------------------------------

def build_system_prompt():
    return (
        "You are a human fiction editor having a conversation with the author.\n"
        "You answer specific questions about the text thoughtfully and honestly.\n\n"
        "RULES:\n"
        "- Do NOT invent canon\n"
        "- Do NOT change memory or facts\n"
        "- If unsure, say so\n"
        "- Give concrete, local advice\n"
        "- You MAY suggest alternative wording\n"
        "- Keep answers focused on the question\n"
        "- Be supportive but intellectually honest\n"
    )


def build_context(chapter_text, summaries, characters):
    context = f"""
CHAPTER (SOURCE TEXT):
{chapter_text}

PAST SUMMARIES (BACKGROUND MEMORY):
{summaries}

CHARACTER MEMORY (REFERENCE ONLY):
{characters}
"""
    return trim(context, MAX_CONTEXT_CHARS)


# ---------------------------------
# INTERACTIVE LOOP
# ---------------------------------

def interactive_session(chapter_name):
    chapter_text = load_chapter(chapter_name)
    summaries = load_summaries()
    characters = load_characters()

    system_prompt = build_system_prompt()
    context = build_context(chapter_text, summaries, characters)

    print("\n🖋️  Editorial Q&A Mode")
    print("Ask questions about this chapter.")
    print("Type 'exit' to quit.\n")

    # ---------- MOCK MODE ----------
    if MOCK_MODE:
        while True:
            user_input = input(">> ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("\nSession ended.\n")
                break

            print(
                "\n[MOCK EDITOR RESPONSE]\n"
                "In live mode, the editor would respond here with a grounded, "
                "chapter-aware answer based on the text, summaries, and character memory.\n"
            )
        return

    # ---------- LIVE MODE ----------
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Here is the context for this conversation.\n"
                "You will answer questions about it.\n\n"
                f"{context}"
            )
        }
    ]

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\nSession ended.\n")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.6
        )

        answer = response.choices[0].message.content
        print("\n" + answer + "\n")

        messages.append({"role": "assistant", "content": answer})


# ---------------------------------
# MAIN
# ---------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/editorial_query.py chapter_000X.txt")
        sys.exit(1)

    chapter_name = sys.argv[1]
    interactive_session(chapter_name)


if __name__ == "__main__":
    main()
