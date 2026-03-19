#!/usr/bin/env python3
"""
Test script demonstrating character arc tracking with the example scenario:
- Simple man doing nothing good
- Mom dies in accident (turning point)
- Period of isolation and frustration
- Inappropriate joking/later flagged as inconsistency
"""

import json
import os
from character_arc_tracker import CharacterArcTracker

def create_test_scenario():
    """Create test chapters demonstrating character arc scenario"""
    
    test_chapters = {
        "chapter_0001": """
        John was a simple man who didn't care much about anything. He spent his days
        lounging around and avoiding responsibility. His friends often tried to get him
        to work harder, but John just laughed and said life was too short to worry.
        He was always joking around with his friends at the local bar, telling stories
        and making everyone laugh. John's mother worried about him constantly.
        """,
        
        "chapter_0002": """
        tragedy struck when John's mother died in a terrible car accident. The news
        came suddenly, and John was completely devastated. He couldn't believe she
        was gone. The funeral was a somber affair, with John barely able to speak.
        He felt completely lost and alone in the world. This was a turning point
        that would change everything for John.
        """,
        
        "chapter_0003": """
        John withdrew from everyone after his mother's death. He stopped going to
        the bar and avoided his friends' calls. He spent most of his time alone
        in his apartment, staring at the walls. The grief was overwhelming, and
        John felt angry at the world for taking his mother. He was frustrated with
        himself and everyone around him. This period of isolation was deep and
        concerning to those who knew him.
        """,
        
        "chapter_0004": """
        John sat alone in his apartment, still grieving his mother's death. The
        pain hadn't lessened after three months. He ignored his friends' attempts
        to reach out, preferring to suffer in silence. The anger and frustration
        continued to build inside him. John's transformation from a carefree man
        to a grieving, isolated soul was complete and tragic to witness.
        """,
        
        "chapter_0005": """
        John was joking and laughing with his friends at the bar again. He was
        telling funny stories and enjoying himself like nothing had happened.
        His friends were confused by this sudden change in behavior, given that
        his mother had only been dead for a few months. John seemed to have
        completely forgotten his grief and was back to his old self.
        """
    }
    
    return test_chapters

def test_arc_tracking():
    """Test the character arc tracking system"""
    
    print("🎭 Testing Character Arc Tracking System")
    print("=" * 60)
    
    # Create test scenario
    test_chapters = create_test_scenario()
    
    # Initialize tracker
    tracker = CharacterArcTracker()
    
    character_name = "John"
    
    print(f"\n📖 Analyzing character arc for {character_name}...")
    
    # Analyze arc development
    phases = tracker.analyze_character_arc_development(character_name, test_chapters)
    
    print(f"\n📊 Character Phases Detected:")
    for i, phase in enumerate(phases, 1):
        print(f"{i}. {phase.phase_name.upper()} (Chapters {phase.chapter_start}-{phase.chapter_end or 'present'})")
        print(f"   Emotional State: {phase.emotional_state}")
        print(f"   Description: {phase.description}")
        print(f"   Triggers: {', '.join(phase.triggers)}")
        print(f"   Confidence: {phase.confidence:.2f}")
        print()
    
    # Extract actions from all chapters
    all_actions = []
    for chapter_id, text in test_chapters.items():
        actions = tracker.extract_character_actions(character_name, chapter_id, text)
        all_actions.extend(actions)
    
    print(f"🎬 Character Actions Extracted:")
    for action in all_actions:
        print(f"  Chapter {action.chapter}: {action.action}")
        print(f"    Emotional Tone: {action.emotional_tone} (confidence: {action.confidence:.2f})")
        print()
    
    # Check consistency
    alerts = tracker.check_thematic_consistency(character_name, phases, all_actions)
    
    print(f"⚠️ CONSISTENCY ALERTS:")
    if alerts:
        for alert in alerts:
            print(f"  🚨 {alert.severity.upper()} ALERT:")
            print(f"     Chapter: {alert.chapter}")
            print(f"     Action: {alert.action}")
            print(f"     Current Phase: {alert.current_phase}")
            print(f"     Expected: {alert.expected_behavior}")
            print(f"     Actual: {alert.actual_behavior}")
            print(f"     Explanation: {alert.explanation}")
            print(f"     Confidence: {alert.confidence:.2f}")
            print()
    else:
        print("  ✅ No inconsistencies detected")
    
    # Save results
    tracker.save_character_arc(character_name, phases)
    tracker.save_consistency_alerts(character_name, alerts)
    
    print(f"📁 Results saved to:")
    print(f"   - Character arc: data/character_arcs/{character_name.lower()}_arc.json")
    print(f"   - Consistency alerts: data/character_arcs/{character_name.lower()}_alerts.json")
    
    return phases, alerts

def demonstrate_with_llm():
    """Demonstrate with LLM analysis (if API key available)"""
    
    print("\n🤖 Testing with LLM Analysis...")
    print("(Note: Requires OpenAI API key for full functionality)")
    
    # You can add your API key here to test LLM analysis
    api_key = None  # Add your key here: "sk-..."
    
    if api_key:
        tracker = CharacterArcTracker(api_key)
        test_chapters = create_test_scenario()
        
        phases = tracker.analyze_character_arc_development("John", test_chapters)
        print("LLM analysis complete!")
    else:
        print("Skipping LLM test - no API key provided")
        print("System will use rule-based analysis instead")

if __name__ == "__main__":
    # Run the test
    phases, alerts = test_arc_tracking()
    
    # Demonstrate LLM capabilities
    demonstrate_with_llm()
    
    print("\n✅ Character Arc Tracking Test Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("  ✅ Phase detection (innocent → grieving → isolated)")
    print("  ✅ Action emotional analysis")
    print("  ✅ Consistency checking (joking after grief flagged)")
    print("  ✅ Severity assessment (major/moderate/minor)")
    print("  ✅ Detailed explanations for each alert")
    print("  ✅ Persistent storage of arc data")
    
    if alerts:
        print(f"\n🎯 System successfully flagged {len(alerts)} thematic inconsistencies!")
    else:
        print(f"\n⚠️ No alerts - check if rule-based analysis needs refinement")
