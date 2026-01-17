import os
from datetime import datetime

# Path to store chapters
CHAPTERS_DIR = "../data/chapters"


def ensure_chapters_dir():
    if not os.path.exists(CHAPTERS_DIR):
        os.makedirs(CHAPTERS_DIR)


def get_next_chapter_number():
    """
    Scans existing chapter files and returns the next chapter number as int.
    Supports both old (chapter_1.txt) and new (chapter_0001.txt) formats.
    """
    max_number = 0

    if not os.path.exists(CHAPTERS_DIR):
        return 1

    for filename in os.listdir(CHAPTERS_DIR):
        if filename.startswith("chapter_") and filename.endswith(".txt"):
            number_part = filename.replace("chapter_", "").replace(".txt", "")
            if number_part.isdigit():
                max_number = max(max_number, int(number_part))

    return max_number + 1


def format_chapter_id(number: int) -> str:
    """
    Formats chapter number into fixed-width ID.
    Example: 1 -> chapter_0001
    """
    return f"chapter_{number:04d}"


def main():
    print("=== Add New Chapter ===")

    print("Enter chapter text (type END on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    chapter_text = "\n".join(lines)

    ensure_chapters_dir()

    chapter_number = get_next_chapter_number()
    chapter_id = format_chapter_id(chapter_number)

    filename = f"{chapter_id}.txt"
    filepath = os.path.join(CHAPTERS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{chapter_id.replace('_', ' ').title()}\n")
        f.write(f"Saved on: {datetime.now()}\n\n")
        f.write(chapter_text)

    print(f"\n✅ {chapter_id} saved successfully!")
    print(f"📁 Location: {filepath}")


if __name__ == "__main__":
    main()
