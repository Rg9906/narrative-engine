import os
from datetime import datetime

# Path to store chapters
CHAPTERS_DIR = "../data/chapters"


def ensure_chapters_dir():
    if not os.path.exists(CHAPTERS_DIR):
        os.makedirs(CHAPTERS_DIR)


def get_next_chapter_number():
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
    return f"chapter_{number:04d}"


def main():
    print("=== Add / Insert Chapter ===")

    ensure_chapters_dir()

    next_number = get_next_chapter_number()
    print(f"Next available chapter number: {next_number}")

    raw = input(
        "Enter chapter number (press Enter to use next): "
    ).strip()

    if raw == "":
        chapter_number = next_number
    else:
        if not raw.isdigit():
            print("❌ Invalid chapter number.")
            return
        chapter_number = int(raw)

    chapter_id = format_chapter_id(chapter_number)

    print("\nEnter chapter text (type END on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    chapter_text = "\n".join(lines)

    filename = f"{chapter_id}.txt"
    filepath = os.path.join(CHAPTERS_DIR, filename)

    if os.path.exists(filepath):
        confirm = input(
            f"\n⚠️ {filename} exists. Overwrite? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("❌ Operation cancelled.")
            return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{chapter_id.replace('_', ' ').title()}\n")
        f.write(f"Saved on: {datetime.now()}\n\n")
        f.write(chapter_text)

    print(f"\n✅ {chapter_id} saved successfully!")
    print(f"📁 Location: {filepath}")


if __name__ == "__main__":
    main()
