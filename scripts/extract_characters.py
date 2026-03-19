import os
import json
import sys
import re
from character_memory_manager import extract_characters_with_improved_method

# =================================================
# PATH CONFIG
# =================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SUMMARIES_DIR = os.path.join(BASE_DIR, "data", "summaries")
CHARACTERS_DIR = os.path.join(BASE_DIR, "data", "characters")

CANDIDATES_PATH = os.path.join(BASE_DIR, "data", "candidates.json")
AMBIGUOUS_FACTS_PATH = os.path.join(BASE_DIR, "data", "ambiguous_facts.json")
UNRESOLVED_REFS_PATH = os.path.join(BASE_DIR, "data", "unresolved_references.json")

# =================================================
# TEXT HELPERS
# =================================================

def load_summary(filename):
    path = os.path.join(SUMMARIES_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Summary not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_into_sentences(text):
    raw = re.split(r"[.!?]\s+", text)
    return [s.strip() for s in raw if s.strip()]

# =================================================
# NAME EXTRACTION
# =================================================

def extract_character_names(text):
    tokens = re.findall(r"\b[A-Z][a-z]{2,}\b", text)

    blacklist = {
        "The", "This", "That", "Chapter", "Summary",
        "He", "She", "His", "Her", "They", "Their",
        "Tension", "Silence", "Darkness", "Night",
        "Day", "Morning", "Evening", "Shadow",
        "Sergeant", "Captain", "Doctor"
    }

    freq = {}
    for t in tokens:
        if t not in blacklist:
            freq[t] = freq.get(t, 0) + 1

    confirmed = []
    pending = []

    for name, count in freq.items():
        if count > 1:
            confirmed.append(name)
        else:
            pending.append(name)

    return confirmed, pending

# =================================================
# CLASSIFICATION RULES
# =================================================

FACT_PATTERNS = [
    r"\bis\b",
    r"\bwas\b",
    r"\bkilled\b",
    r"\bmurderer\b",
    r"\bresponsible\b",
    r"\bconfessed\b",
]

QUESTION_PATTERNS = [
    "why", "unclear", "unknown", "wonders", "question", "mystery"
]

PRONOUNS = {"he", "she", "him", "her"}

TITLE_PATTERNS = [
    r"\bMr\.?\s+[A-Z][a-z]+\b",
    r"\bMrs\.?\s+[A-Z][a-z]+\b",
    r"\bMiss\s+[A-Z][a-z]+\b",
]

ROLE_TERMS = {
    "my master",
    "my mistress",
    "madam",
    "sir"
}

# =================================================
# UTILS
# =================================================

def is_established_fact(sentence):
    s = sentence.lower()
    return any(re.search(p, s) for p in FACT_PATTERNS)


def is_open_question(sentence):
    s = sentence.lower()
    return any(q in s for q in QUESTION_PATTERNS)


def contains_pronoun(sentence):
    return any(p in sentence.lower().split() for p in PRONOUNS)


def extract_unresolved_references(sentence):
    refs = []

    for p in TITLE_PATTERNS:
        refs.extend(re.findall(p, sentence))

    for role in ROLE_TERMS:
        if role in sentence.lower():
            refs.append(role)

    return refs

# =================================================
# FILE HELPERS
# =================================================

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_or_create_character(name, chapter_id):
    path = os.path.join(CHARACTERS_DIR, f"{name.lower()}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), path

    character = {
        "name": name,
        "aliases": [],          # 👈 NEW (manual only)
        "titles": [],           # 👈 OPTIONAL metadata
        "first_appearance": chapter_id,
        "established_facts": [],
        "observed_behaviors": [],
        "open_questions": [],
        "relationships": {},
        "last_updated": chapter_id
    }

    return character, path


def save_character(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character, f, indent=2, ensure_ascii=False)

# =================================================
# MAIN
# =================================================

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_characters.py chapter_XXXX_summary.txt")
        sys.exit(1)

    summary_file = sys.argv[1]
    
    # Use the improved character memory manager
    print("🔍 Using improved character extraction with context awareness...")
    extract_characters_with_improved_method(summary_file)
    
    # Also run the original extraction for comparison (optional)
    print("\n📊 Running original extraction for comparison...")
    chapter_id = summary_file.replace("_summary.txt", "")

    os.makedirs(CHARACTERS_DIR, exist_ok=True)

    text = load_summary(summary_file)
    sentences = split_into_sentences(text)

    confirmed, pending = extract_character_names(text)

    # ---- candidates ----
    candidates = load_json(CANDIDATES_PATH)
    if pending:
        candidates.setdefault(chapter_id, [])
        for p in pending:
            if p not in candidates[chapter_id]:
                candidates[chapter_id].append(p)
        save_json(CANDIDATES_PATH, candidates)

    # ---- preload characters ----
    characters = {}
    for name in confirmed:
        characters[name], _ = load_or_create_character(name, chapter_id)

    last_explicit = None
    ambiguous_facts = load_json(AMBIGUOUS_FACTS_PATH)
    unresolved_refs = load_json(UNRESOLVED_REFS_PATH)

    # ---- sentence processing ----
    for sentence in sentences:
        mentioned = [n for n in confirmed if n in sentence]

        # unresolved references (titles / roles)
        refs = extract_unresolved_references(sentence)
        if refs:
            unresolved_refs.setdefault(chapter_id, [])
            unresolved_refs[chapter_id].append({
                "sentence": sentence,
                "references": refs
            })

        # explicit name
        if len(mentioned) == 1:
            name = mentioned[0]
            last_explicit = name
            character = characters[name]

        # safe pronoun attribution
        elif last_explicit and contains_pronoun(sentence) and not mentioned:
            character = characters[last_explicit]

        # ambiguous critical fact
        elif contains_pronoun(sentence) and is_established_fact(sentence):
            ambiguous_facts.setdefault(chapter_id, [])
            if sentence not in ambiguous_facts[chapter_id]:
                ambiguous_facts[chapter_id].append(sentence)
            continue
        else:
            continue

        if is_open_question(sentence):
            character["open_questions"].append(sentence)
        elif is_established_fact(sentence):
            character["established_facts"].append(sentence)
        else:
            character["observed_behaviors"].append({
                "chapter": chapter_id,
                "behavior": sentence
            })

    # ---- save ----
    for name, c in characters.items():
        c["last_updated"] = chapter_id
        save_character(c, os.path.join(CHARACTERS_DIR, f"{name.lower()}.json"))

    save_json(AMBIGUOUS_FACTS_PATH, ambiguous_facts)
    save_json(UNRESOLVED_REFS_PATH, unresolved_refs)

    print("Extraction complete.")
    if unresolved_refs.get(chapter_id):
        print("⚠️ Unresolved references stored for review.")


if __name__ == "__main__":
    main()
