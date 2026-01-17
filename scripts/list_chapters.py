import os

CHAPTERS_DIR = "../data/chapters"


def main():
    print("=== Stored Chapters ===")

    if not os.path.exists(CHAPTERS_DIR):
        print("No chapters directory found.")
        return

    files = os.listdir(CHAPTERS_DIR)

    chapter_files = [
        f for f in files
        if f.startswith("chapter_") and f.endswith(".txt")
    ]

    if not chapter_files:
        print("No chapters stored yet.")
        return

    chapter_files.sort()

    for filename in chapter_files:
        filepath = os.path.join(CHAPTERS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

        print(f"- {filename} → {first_line}")


if __name__ == "__main__":
    main()
