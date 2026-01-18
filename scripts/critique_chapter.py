import os
import sys
from openai import OpenAI

# =================================================
# PATH SETUP (PIPELINE-SAFE)
# =================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "data", "chapters")
SUMMARIES_DIR = os.path.join(BASE_DIR, "data", "summaries")
EVALUATIONS_DIR = os.path.join(BASE_DIR, "data", "evaluations")

client = OpenAI()

# =================================================
# LOADERS
# =================================================

def load_chapter(chapter_number):
    path = os.path.join(CHAPTERS_DIR, f"chapter_{chapter_number}.txt")

    if not os.path.exists(path):
        print("❌ Chapter not found.")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_all_summaries():
    if not os.path.exists(SUMMARIES_DIR):
        return []

    summaries = []
    for filename in os.listdir(SUMMARIES_DIR):
        if filename.endswith("_summary.txt"):
            path = os.path.join(SUMMARIES_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                summaries.append(f"{filename}:\n{f.read()}")

    return summaries

# =================================================
# AI HELPERS
# =================================================

def select_relevant_summaries(chapter_text, all_summaries):
    prompt = (
        "Given the following new chapter and past chapter summaries, "
        "list which summaries are most relevant to check for consistency. "
        "Return ONLY the filenames, separated by commas.\n\n"
        "PAST SUMMARIES:\n"
        f"{chr(10).join(all_summaries)}\n\n"
        "NEW CHAPTER:\n"
        f"{chapter_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a careful narrative analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def critique(chapter_text, relevant_summaries):
    context = "\n\n".join(relevant_summaries)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict literary critic. "
                    "Analyze the new chapter for:\n"
                    "- consistency with past events\n"
                    "- character behavior and development\n"
                    "- tone and thematic alignment\n"
                    "- logical or timeline contradictions\n\n"
                    "Be specific and constructive."
                )
            },
            {
                "role": "user",
                "content": (
                    "PAST CONTEXT (RELEVANT SUMMARIES):\n"
                    f"{context}\n\n"
                    "NEW CHAPTER:\n"
                    f"{chapter_text}\n\n"
                    "Provide a structured critique."
                )
            }
        ]
    )

    return response.choices[0].message.content.strip()

# =================================================
# MAIN
# =================================================

def main():
    print("=== Critique Chapter ===")

    if len(sys.argv) > 1:
        chapter_number = sys.argv[1].replace("chapter_", "").replace(".txt", "")
    else:
        chapter_number = input("Enter chapter number to critique: ").strip()

    chapter_text = load_chapter(chapter_number)
    if chapter_text is None:
        return

    all_summaries = load_all_summaries()

    if not all_summaries:
        print("⚠️ No summaries found. Critique may be shallow.")
        relevant_summaries = []
    else:
        print("🔍 Selecting relevant past context...")
        relevant_names = select_relevant_summaries(chapter_text, all_summaries)

        relevant_summaries = [
            s for s in all_summaries
            if any(name.strip() in s for name in relevant_names.split(","))
        ]

    print("🧠 Generating critique...\n")
    result = critique(chapter_text, relevant_summaries)

    print("=== CRITIQUE ===\n")
    print(result)

    # ---------- PERSIST CRITIQUE FOR UI ----------

    os.makedirs(EVALUATIONS_DIR, exist_ok=True)

    out_path = os.path.join(
        EVALUATIONS_DIR,
        f"chapter_{chapter_number}_critique.txt"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"[OK] Critique saved to {out_path}")


if __name__ == "__main__":
    main()
