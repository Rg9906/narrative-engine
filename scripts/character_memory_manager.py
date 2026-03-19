import json
import os
from typing import Dict, Set, List
from improved_entity_extractor import ImprovedEntityExtractor

class CharacterMemoryManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.characters_dir = os.path.join(data_dir, "characters")
        self.candidates_path = os.path.join(data_dir, "candidates.json")
        self.established_path = os.path.join(data_dir, "established_characters.json")
        
        self.extractor = ImprovedEntityExtractor()
        self.established_characters = self.load_established_characters()
        
    def load_established_characters(self) -> Set[str]:
        """Load previously confirmed characters"""
        if os.path.exists(self.established_path):
            with open(self.established_path, 'r') as f:
                data = json.load(f)
                return set(data.get('characters', []))
        return set()
    
    def save_established_characters(self):
        """Save confirmed characters to file"""
        os.makedirs(os.path.dirname(self.established_path), exist_ok=True)
        with open(self.established_path, 'w') as f:
            json.dump({'characters': list(self.established_characters)}, f, indent=2)
    
    def update_character_memory(self, chapter_text: str, chapter_id: str):
        """Update character memory with new chapter"""
        # Extract characters using context-aware method
        character_data, pronoun_map = self.extractor.extract_characters_with_context(
            chapter_text, self.established_characters
        )
        
        # Get confidence scores
        confidence_scores = self.extractor.get_character_confidence_scores(character_data)
        
        # Separate high-confidence from candidates
        confirmed = []
        candidates = []
        
        for name, score in confidence_scores.items():
            if score >= 1.5 or name in self.established_characters:  # Confidence threshold
                confirmed.append(name)
            else:
                candidates.append(name)
        
        # Update established characters
        new_characters = set(confirmed) - self.established_characters
        if new_characters:
            self.established_characters.update(new_characters)
            self.save_established_characters()
            print(f"[+] New characters established: {', '.join(new_characters)}")
        
        # Save candidates for review
        self.save_candidates(candidates, chapter_id, confidence_scores)
        
        # Update individual character files
        self.update_character_files(character_data, chapter_id)
        
        return confirmed, candidates
    
    def save_candidates(self, candidates: List[str], chapter_id: str, 
                       confidence_scores: Dict[str, float]):
        """Save potential characters for manual review"""
        existing_candidates = {}
        if os.path.exists(self.candidates_path):
            with open(self.candidates_path, 'r') as f:
                existing_candidates = json.load(f)
        
        chapter_candidates = []
        for name in candidates:
            chapter_candidates.append({
                'name': name,
                'confidence': confidence_scores[name],
                'chapter': chapter_id
            })
        
        existing_candidates[chapter_id] = chapter_candidates
        
        with open(self.candidates_path, 'w') as f:
            json.dump(existing_candidates, f, indent=2)
    
    def update_character_files(self, character_data: Dict, chapter_id: str):
        """Update individual character JSON files"""
        os.makedirs(self.characters_dir, exist_ok=True)
        
        for character_name, data in character_data.items():
            if character_name not in self.established_characters:
                continue
                
            char_file = os.path.join(self.characters_dir, f"{character_name.lower()}.json")
            
            # Load existing character data or create new
            if os.path.exists(char_file):
                with open(char_file, 'r') as f:
                    char_data = json.load(f)
            else:
                char_data = {
                    'name': character_name,
                    'first_appearance': chapter_id,
                    'established_facts': [],
                    'observed_behaviors': [],
                    'open_questions': [],
                    'relationships': {},
                    'last_updated': chapter_id
                }
            
            # Update with new information
            self.process_character_contexts(char_data, data, chapter_id)
            char_data['last_updated'] = chapter_id
            
            # Save updated character data
            with open(char_file, 'w') as f:
                json.dump(char_data, f, indent=2)
    
    def process_character_contexts(self, char_data: Dict, new_data: Dict, chapter_id: str):
        """Process new contexts and categorize them"""
        contexts = new_data['contexts']
        
        for context in contexts:
            # Skip pronoun contexts for facts (they're behaviors)
            if context.startswith('[PRONOUN]'):
                context = context.replace('[PRONOUN]', '').strip()
                char_data['observed_behaviors'].append({
                    'chapter': chapter_id,
                    'behavior': context,
                    'type': 'pronoun_reference'
                })
                continue
            
            # Categorize based on content patterns
            context_lower = context.lower()
            
            # Check for established facts
            if any(verb in context_lower for verb in ['is', 'was', 'are', 'were']):
                if context not in char_data['established_facts']:
                    char_data['established_facts'].append(context)
            
            # Check for questions or mysteries
            elif any(word in context_lower for word in ['wonder', 'question', 'mystery', 'unclear']):
                if context not in char_data['open_questions']:
                    char_data['open_questions'].append(context)
            
            # Otherwise, treat as observed behavior
            else:
                char_data['observed_behaviors'].append({
                    'chapter': chapter_id,
                    'behavior': context,
                    'type': 'observed_action'
                })
    
    def get_character_summary(self, character_name: str) -> Dict:
        """Get summary of character information"""
        if character_name not in self.established_characters:
            return {'error': f'Character {character_name} not found'}
        
        char_file = os.path.join(self.characters_dir, f"{character_name.lower()}.json")
        if os.path.exists(char_file):
            with open(char_file, 'r') as f:
                return json.load(f)
        
        return {'error': f'Character file for {character_name} not found'}
    
    def review_candidates(self) -> Dict:
        """Get candidates pending review"""
        if os.path.exists(self.candidates_path):
            with open(self.candidates_path, 'r') as f:
                return json.load(f)
        return {}
    
    def confirm_character(self, character_name: str):
        """Manually confirm a character from candidates"""
        if character_name not in self.established_characters:
            self.established_characters.add(character_name)
            self.save_established_characters()
            
            # Create character file
            char_file = os.path.join(self.characters_dir, f"{character_name.lower()}.json")
            if not os.path.exists(char_file):
                char_data = {
                    'name': character_name,
                    'first_appearance': 'manual_confirmation',
                    'established_facts': [],
                    'observed_behaviors': [],
                    'open_questions': [],
                    'relationships': {},
                    'last_updated': 'manual_confirmation'
                }
                with open(char_file, 'w') as f:
                    json.dump(char_data, f, indent=2)
            
            print(f"[✓] Character confirmed: {character_name}")
            return True
        return False

# Integration function to replace extract_characters.py
def extract_characters_with_improved_method(summary_file: str):
    """Drop-in replacement for extract_characters.py main function"""
    import sys
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    manager = CharacterMemoryManager(data_dir)
    
    # Load summary text
    summaries_dir = os.path.join(data_dir, "summaries")
    summary_path = os.path.join(summaries_dir, summary_file)
    
    if not os.path.exists(summary_path):
        print(f"❌ Summary file not found: {summary_path}")
        return
    
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary_text = f.read()
    
    chapter_id = summary_file.replace("_summary.txt", "")
    
    print(f"🔍 Processing character extraction for {chapter_id}")
    
    # Update character memory
    confirmed, candidates = manager.update_character_memory(summary_text, chapter_id)
    
    print(f"[✓] Confirmed characters: {', '.join(confirmed) if confirmed else 'None'}")
    print(f"[?] Candidates for review: {', '.join(candidates) if candidates else 'None'}")
    
    if candidates:
        print(f"\n📋 Review candidates in: {manager.candidates_path}")
        print("Use CharacterMemoryManager.confirm_character(name) to confirm any of these.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python character_memory_manager.py chapter_XXXX_summary.txt")
        sys.exit(1)
    
    extract_characters_with_improved_method(sys.argv[1])
