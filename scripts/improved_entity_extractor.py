import re
import json
from typing import List, Tuple, Dict, Set
from collections import defaultdict

class ImprovedEntityExtractor:
    def __init__(self):
        # Enhanced blacklist with context
        self.stop_words = {
            # Common sentence starters
            "The", "This", "That", "These", "Those", "Their", "There", "Then",
            "Chapter", "Summary", "Prologue", "Epilogue",
            # Time/place words
            "Morning", "Evening", "Night", "Day", "Today", "Tomorrow", "Yesterday",
            "Spring", "Summer", "Fall", "Winter", "April", "May", "June", "July",
            # Common nouns that appear capitalized
            "Darkness", "Light", "Shadow", "Silence", "Tension", "Mystery",
            "House", "Room", "Door", "Window", "Garden", "Street",
            # Titles/honorifics (handle separately)
            "Mr", "Mrs", "Miss", "Sir", "Madam", "Doctor", "Sergeant", "Captain"
        }
        
        # Ambiguous words that could be names OR common nouns
        self.ambiguous_words = {
            "May", "June", "Lily", "Rose", "Jack", "Bill", "Will", "Mark",
            "Hope", "Grace", "Faith", "Joy", "Ruby", "Jade", "Ivy"
        }
        
        # Name-like patterns
        self.name_pattern = r"\b[A-Z][a-z]{2,}\b"
        
        # Context clues for character names
        self.character_context_patterns = [
            r"\bsaid\b",
            r"\bthought\b",
            r"\bfelt\b",
            r"\blooked\b",
            r"\bwalked\b",
            r"\braised\b",
            r"\bturned\b",
            r"\bsmiled\b",
            r"\bfrowned\b",
            r"\breplied\b"
        ]

    def extract_potential_names(self, text: str) -> List[str]:
        """Extract all capitalized words that could be names"""
        candidates = re.findall(self.name_pattern, text)
        return [word for word in candidates if word not in self.stop_words]

    def is_likely_character_name(self, word: str, sentence: str, 
                                established_characters: Set[str]) -> bool:
        """Determine if a word is likely a character name based on context"""
        
        # If already established as character, it's definitely a name
        if word in established_characters:
            return True
        
        # Check for character actions in the same sentence
        has_character_action = any(
            re.search(pattern, sentence, re.IGNORECASE) 
            for pattern in self.character_context_patterns
        )
        
        # Check for possessive forms (character's)
        possessive_pattern = rf"\b{word}'s\b"
        has_possessive = re.search(possessive_pattern, sentence)
        
        # Check for dialogue patterns
        dialogue_pattern = rf'{word}.*?"'
        has_dialogue = re.search(dialogue_pattern, sentence)
        
        # Ambiguous words need more context
        if word in self.ambiguous_words:
            return has_character_action or has_possessive or has_dialogue
        
        # Non-ambiguous words are more likely names if they pass basic checks
        return has_character_action or has_possessive

    def resolve_pronouns(self, sentences: List[str], 
                        character_mentions: Dict[str, List[int]]) -> Dict[int, str]:
        """Resolve pronouns to most recent character"""
        pronoun_map = {}
        last_character = None
        
        for i, sentence in enumerate(sentences):
            # Find explicit character mentions in this sentence
            mentioned_chars = []
            for char in character_mentions.keys():
                if char in sentence:
                    mentioned_chars.append(char)
            
            if mentioned_chars:
                # Update last mentioned character
                last_character = mentioned_chars[0]  # Take first mention
            
            # Check for pronouns
            pronouns = re.findall(r"\b(he|she|him|her|his|hers)\b", sentence, re.IGNORECASE)
            if pronouns and last_character:
                pronoun_map[i] = last_character
        
        return pronoun_map

    def extract_characters_with_context(self, text: str, 
                                      established_characters: Set[str] = None) -> Tuple[Dict, Dict]:
        """Main extraction method with context awareness"""
        if established_characters is None:
            established_characters = set()
        
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        character_data = defaultdict(lambda: {
            'mentions': [],
            'contexts': [],
            'actions': [],
            'relationships': set()
        })
        
        # Track which sentences mention which characters
        character_mentions = defaultdict(list)
        
        for i, sentence in enumerate(sentences):
            potential_names = self.extract_potential_names(sentence)
            
            for name in potential_names:
                if self.is_likely_character_name(name, sentence, established_characters):
                    character_data[name]['mentions'].append(i)
                    character_data[name]['contexts'].append(sentence)
                    character_mentions[name].append(i)
        
        # Resolve pronouns
        pronoun_resolution = self.resolve_pronouns(sentences, character_mentions)
        
        # Add pronoun contexts to character data
        for sentence_idx, character in pronoun_resolution.items():
            character_data[character]['mentions'].append(sentence_idx)
            character_data[character]['contexts'].append(f"[PRONOUN] {sentences[sentence_idx]}")
        
        return dict(character_data), pronoun_resolution

    def get_character_confidence_scores(self, character_data: Dict) -> Dict[str, float]:
        """Calculate confidence scores for each potential character"""
        scores = {}
        
        for name, data in character_data.items():
            score = 0.0
            
            # Base score for mentions
            mention_count = len(set(data['mentions']))
            score += min(mention_count * 0.3, 2.0)  # Max 2 points for mentions
            
            # Context diversity bonus
            unique_contexts = len(set(data['contexts']))
            score += min(unique_contexts * 0.2, 1.0)  # Max 1 point for diversity
            
            # Pronoun resolution bonus
            pronoun_refs = sum(1 for ctx in data['contexts'] if ctx.startswith('[PRONOUN]'))
            score += min(pronoun_refs * 0.1, 0.5)  # Max 0.5 points for pronouns
            
            # Action verb bonus
            action_sentences = sum(1 for ctx in data['contexts'] 
                                 if any(verb in ctx.lower() 
                                       for verb in ['said', 'thought', 'felt', 'looked', 'walked']))
            score += min(action_sentences * 0.15, 0.5)  # Max 0.5 points for actions
            
            scores[name] = score
        
        return scores

# Usage example
if __name__ == "__main__":
    extractor = ImprovedEntityExtractor()
    
    # Test with your narrative text
    sample_text = """
    Giselle sat beside the easel in her small room. She dipped her brush in white paint.
    Laurie stood at the edge of the garden. He watched the children play. May walked over
    to the window. The morning light was bright. She thought about the conversation.
    """
    
    established_chars = {"Giselle", "Laurie"}  # From previous chapters
    
    character_data, pronoun_map = extractor.extract_characters_with_context(
        sample_text, established_chars
    )
    
    confidence_scores = extractor.get_character_confidence_scores(character_data)
    
    print("Potential Characters:")
    for name, score in sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{name}: {score:.2f} (mentions: {len(character_data[name]['mentions'])})")
    
    print("\nPronoun Resolution:")
    for sent_idx, character in pronoun_map.items():
        print(f"Sentence {sent_idx}: {character}")
