import os
from openai import OpenAI

# Directories
CHAPTERS_DIR = "../data/chapters"
SUMMARIES_DIR = "../data/summaries"

client = OpenAI()


def ensure_summaries_dir():
    if not os.path.exists(SUMMARIES_DIR):
        os.makedirs(SUMMARIES_DIR)


def load_chapter(chapter_number):
    filename = f"chapter_{chapter_number}.txt"
    filepath = os.path.join(CHAPTERS_DIR, filename)

    if not os.path.exists(filepath):
        print("❌ Chapter not found.")
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


def main():
    print("=== Summarize Chapter ===")
    chapter_number = input("Enter chapter number to summarize: ").strip()

    chapter_text = load_chapter(chapter_number)
    if chapter_text is None:
        return

    print("🧠 Generating summary...")
    summary = summarize_text(chapter_text)

    ensure_summaries_dir()

    summary_filename = f"chapter_{chapter_number}_summary.txt"
    summary_path = os.path.join(SUMMARIES_DIR, summary_filename)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Summary saved: {summary_path}\n")
    print("=== Summary ===")
    print(summary)


if __name__ == "__main__":
    main()
