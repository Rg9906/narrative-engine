import os
from openai import OpenAI

# Directories
CHAPTERS_DIR = "../data/chapters"
SUMMARIES_DIR = "../data/summaries"

client = OpenAI()


def load_chapter(chapter_number):
    """Load the full text of a chapter."""
    path = os.path.join(CHAPTERS_DIR, f"chapter_{chapter_number}.txt")

    if not os.path.exists(path):
        print("❌ Chapter not found.")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_all_summaries():
    """Load all stored chapter summaries."""
    if not os.path.exists(SUMMARIES_DIR):
        return []

    summaries = []
    for filename in os.listdir(SUMMARIES_DIR):
        if filename.endswith("_summary.txt"):
            path = os.path.join(SUMMARIES_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                summaries.append(f"{filename}:\n{f.read()}")

    return summaries


def select_relevant_summaries(chapter_text, all_summaries):
    """
    Ask the AI which past summaries are relevant
    for checking consistency with the new chapter.
    """
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
    """Generate a critique using only relevant past context."""
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


def main():
    print("=== Critique Chapter ===")
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


if __name__ == "__main__":
    main()
