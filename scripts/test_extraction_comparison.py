#!/usr/bin/env python3
"""
Test script to compare old vs new character extraction methods
"""

import sys
import os
import json
from improved_entity_extractor import ImprovedEntityExtractor
from character_memory_manager import CharacterMemoryManager

def test_extraction_methods():
    """Test the extraction methods with challenging examples"""
    
    # Test cases that would break the old system
    test_texts = [
        {
            "name": "Edge case: May as name vs month",
            "text": "May walked into the room. She looked around. The month of May was always beautiful."
        },
        {
            "name": "Edge case: June as name vs month", 
            "text": "June sat by the window. She watched the children play. June had always been her favorite month."
        },
        {
            "name": "Edge case: Lily as name vs flower",
            "text": "Lily picked up the lily from the vase. She smelled the flower. Lily was her name."
        },
        {
            "name": "Pronoun resolution test",
            "text": "Giselle picked up her brush. She painted carefully. The artist was focused on her work."
        },
        {
            "name": "Multiple characters with actions",
            "text": "Giselle said hello to Laurie. He smiled back. She then turned to Sebastian, who nodded politely."
        },
        {
            "name": "False positive prevention",
            "text": "The morning light was bright. Darkness fell across the room. The Shadow moved silently."
        }
    ]
    
    extractor = ImprovedEntityExtractor()
    
    print("=" * 60)
    print("CHARACTER EXTRACTION COMPARISON TEST")
    print("=" * 60)
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"📝 Text: {test_case['text']}")
        
        # Test with no established characters (first chapter scenario)
        character_data, pronoun_map = extractor.extract_characters_with_context(test_case['text'])
        confidence_scores = extractor.get_character_confidence_scores(character_data)
        
        print("\n🎯 Potential Characters Detected:")
        for name, score in sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True):
            contexts = character_data[name]['contexts'][:2]  # Show first 2 contexts
            print(f"  • {name}: {score:.2f}")
            for ctx in contexts:
                print(f"    - {ctx[:60]}...")
        
        print(f"\n🔗 Pronoun Resolution:")
        for sent_idx, character in pronoun_map.items():
            print(f"  • Sentence {sent_idx} → {character}")
        
        print("-" * 40)

def test_with_real_data():
    """Test with actual chapter data"""
    print("\n🔍 TESTING WITH REAL CHAPTER DATA")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    manager = CharacterMemoryManager(data_dir)
    
    # Test with chapter 1
    summaries_dir = os.path.join(data_dir, "summaries")
    chapter_files = [f for f in os.listdir(summaries_dir) if f.endswith("_summary.txt")]
    
    for chapter_file in sorted(chapter_files)[:2]:  # Test first 2 chapters
        print(f"\n📖 Processing {chapter_file}")
        
        summary_path = os.path.join(summaries_dir, chapter_file)
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_text = f.read()
        
        chapter_id = chapter_file.replace("_summary.txt", "")
        
        # Extract with improved method
        character_data, pronoun_map = manager.extractor.extract_characters_with_context(
            summary_text, manager.established_characters
        )
        
        confidence_scores = manager.extractor.get_character_confidence_scores(character_data)
        
        print(f"  Established characters: {manager.established_characters}")
        print(f"  High confidence detections:")
        for name, score in sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True):
            if score >= 1.0:
                mentions = len(set(character_data[name]['mentions']))
                print(f"    • {name}: {score:.2f} ({mentions} mentions)")

def show_current_system_status():
    """Show the current status of the character system"""
    print("\n📊 CURRENT SYSTEM STATUS")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    # Established characters
    established_path = os.path.join(data_dir, "established_characters.json")
    if os.path.exists(established_path):
        with open(established_path, 'r') as f:
            established = json.load(f)
        print(f"✅ Established characters: {', '.join(established['characters'])}")
    
    # Candidates for review
    candidates_path = os.path.join(data_dir, "candidates.json")
    if os.path.exists(candidates_path):
        with open(candidates_path, 'r') as f:
            candidates = json.load(f)
        total_candidates = sum(len(chapter_candidates) for chapter_candidates in candidates.values())
        print(f"🤔 Pending candidates: {total_candidates} across {len(candidates)} chapters")
    
    # Character files
    characters_dir = os.path.join(data_dir, "characters")
    if os.path.exists(characters_dir):
        character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
        print(f"📁 Character files: {len(character_files)}")

if __name__ == "__main__":
    print("🚀 Testing Improved Character Extraction System")
    
    # Show current status
    show_current_system_status()
    
    # Test with edge cases
    test_extraction_methods()
    
    # Test with real data
    test_with_real_data()
    
    print("\n✅ Testing complete!")
    print("\n💡 Key improvements:")
    print("  • Context-aware name detection")
    print("  • Confidence scoring for potential characters")
    print("  • Pronoun resolution to most recent character")
    print("  • Handles ambiguous words (May, June, Lily) with context")
    print("  • Filters out false positives (The, Morning, Darkness)")
    print("  • Learning from established characters")
