import os
from datetime import datetime

# Path to store chapters
CHAPTERS_DIR = "../data/chapters"


def ensure_chapters_dir():
    if not os.path.exists(CHAPTERS_DIR):
        os.makedirs(CHAPTERS_DIR)


def main():
    print("=== Add New Chapter ===")

    chapter_number = input("Enter chapter number: ").strip()

    print("Enter chapter text (type END on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    chapter_text = "\n".join(lines)

    ensure_chapters_dir()

    filename = f"chapter_{chapter_number}.txt"
    filepath = os.path.join(CHAPTERS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Chapter {chapter_number}\n")
        f.write(f"Saved on: {datetime.now()}\n\n")
        f.write(chapter_text)

    print(f"\n✅ Chapter {chapter_number} saved successfully!")
    print(f"📁 Location: {filepath}")


if __name__ == "__main__":
    main()
