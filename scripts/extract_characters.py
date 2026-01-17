import os
import json
import sys
import re

# -------------------------------------------------
# PATH CONFIG (matches your project exactly)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SUMMARIES_DIR = os.path.join(BASE_DIR, "data", "summaries")
CHARACTERS_DIR = os.path.join(BASE_DIR, "data", "characters")

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def load_summary(filename):
    path = os.path.join(SUMMARIES_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Summary not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_character_names(text):
    """
    Very conservative name detection:
    - Capitalized words
    - At least 3 letters
    """
    candidates = set(re.findall(r"\b[A-Z][a-z]{2,}\b", text))

    blacklist = {
        "The", "This", "That", "Chapter", "Summary",
        "He", "She", "His", "Her", "They", "Their"
    }

    return [name for name in candidates if name not in blacklist]


def load_or_create_character(name, chapter_id):
    filename = f"{name.lower()}.json"
    path = os.path.join(CHARACTERS_DIR, filename)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), path

    # New character file
    character = {
        "name": name,
        "first_appearance": chapter_id,
        "core_traits": [],
        "established_facts": [],
        "observed_behaviors": [],
        "relationships": {},
        "open_questions": [],
        "last_updated": chapter_id
    }

    return character, path


def save_character(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character, f, indent=2, ensure_ascii=False)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_characters.py chapter_XX_summary.txt")
        sys.exit(1)

    summary_filename = sys.argv[1]
    chapter_id = summary_filename.replace("_summary.txt", "")

    os.makedirs(CHARACTERS_DIR, exist_ok=True)

    summary_text = load_summary(summary_filename)
    character_names = extract_character_names(summary_text)

    if not character_names:
        print("No characters detected.")
        return

    print("Detected characters:")
    for name in character_names:
        print(" -", name)

    for name in character_names:
        character, path = load_or_create_character(name, chapter_id)

        character["observed_behaviors"].append({
            "chapter": chapter_id,
            "behavior": "Appears in chapter summary"
        })

        character["last_updated"] = chapter_id

        save_character(character, path)
        print(f"Updated: data/characters/{name.lower()}.json")


if __name__ == "__main__":
    main()
