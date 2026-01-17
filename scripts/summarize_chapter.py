import os
from openai import OpenAI

# -------------------------------------------------
# PATH CONFIG (ROBUST)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "data", "chapters")
SUMMARIES_DIR = os.path.join(BASE_DIR, "data", "summaries")

client = OpenAI()

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def ensure_summaries_dir():
    if not os.path.exists(SUMMARIES_DIR):
        os.makedirs(SUMMARIES_DIR)


def format_chapter_id(number: int) -> str:
    """
    1 -> chapter_0001
    """
    return f"chapter_{number:04d}"


def load_chapter(chapter_id):
    filename = f"{chapter_id}.txt"
    filepath = os.path.join(CHAPTERS_DIR, filename)

    if not os.path.exists(filepath):
        print(f"❌ Chapter not found: {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a literary analyst. Summarize the chapter clearly and concisely."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content.strip()

# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():
    print("=== Summarize Chapter ===")

    raw = input("Enter chapter number to summarize (numeric): ").strip()
    if not raw.isdigit():
        print("❌ Invalid chapter number.")
        return

    chapter_number = int(raw)
    chapter_id = format_chapter_id(chapter_number)

    print(f"📘 Loading {chapter_id}...")

    chapter_text = load_chapter(chapter_id)
    if chapter_text is None:
        return

    print("🧠 Generating summary...")
    summary = summarize_text(chapter_text)

    ensure_summaries_dir()

    summary_filename = f"{chapter_id}_summary.txt"
    summary_path = os.path.join(SUMMARIES_DIR, summary_filename)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"\n✅ Summary saved: {summary_path}")
    print("\n=== Summary ===")
    print(summary)


if __name__ == "__main__":
    main()
