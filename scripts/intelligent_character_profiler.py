import re
import json
import os
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from openai import OpenAI

@dataclass
class CharacterProfile:
    """Intelligent character profile structure"""
    name: str
    core_identity: List[str]  # Who they are fundamentally
    personality_traits: List[str]  # How they behave
    physical_attributes: List[str]  # What they look like
    relationships: Dict[str, str]  # Who they know and how
    motivations: List[str]  # What drives them
    conflicts: List[str]  # Internal/external struggles
    skills_abilities: List[str]  # What they can do
    significant_events: List[str]  # Key plot moments
    narrative_role: str  # Their function in story
    character_arc: List[str]  # How they change/develop

class IntelligentCharacterProfiler:
    def __init__(self, api_key=None):
        self.client = OpenAI() if api_key else None
        self.established_characters = set()
        
        # Patterns for different types of character information
        self.trait_patterns = {
            'physical': [
                r'\b(tall|short|thin|heavy|slender|muscular|frail)\b',
                r'\b(hair|eyes|face|skin|hands)\s+\w+',
                r'\b(blond|brunette|redhead|bald|gray)\b',
                r'\b(blue|green|brown|hazel|gray)\s+eyes\b'
            ],
            'personality': [
                r'\b(kind|cruel|gentle|harsh|warm|cold|shy|outgoing)\b',
                r'\b(intelligent|wise|naive|cunning|honest|deceitful)\b',
                r'\b(brave|cowardly|confident|insecure|proud|humble)\b',
                r'\b(patient|impatient|calm|angry|cheerful|melancholy)\b'
            ],
            'actions': [
                r'\b(said|thought|felt|looked|walked|ran|sat|stood)\b',
                r'\b(painted|wrote|sang|danced|fought|cried|laughed)\b',
                r'\b(whispered|shouted|muttered|declared|explained)\b'
            ],
            'relationships': [
                r'\b(mother|father|brother|sister|son|daughter|husband|wife)\b',
                r'\b(friend|enemy|lover|rival|ally|mentor)\b',
                r'\b(love|hate|trust|betray|protect|abandon)\b'
            ]
        }
        
        # Significant narrative indicators
        self.narrative_patterns = {
            'conflict': [
                r'\b(struggle|fight|argue|conflict|tension|disagreement)\b',
                r'\b(afraid|scared|worried|anxious|nervous)\b',
                r'\b(anger|rage|fury|resentment|jealousy)\b'
            ],
            'motivation': [
                r'\b(want|need|desire|wish|hope|dream)\b',
                r'\b(goal|purpose|mission|duty|responsibility)\b',
                r'\b(because|since|reason|why)\b'
            ],
            'change': [
                r'\b(changed|became|transformed|grew|learned)\b',
                r'\b(realized|understood|discovered|found)\b',
                r'\b(before|after|used to|now)\b'
            ]
        }

    def extract_character_insights(self, text: str, character_name: str) -> CharacterProfile:
        """Extract meaningful character insights using pattern matching and AI analysis"""
        
        # Split text into sentences for analysis
        sentences = re.split(r'[.!?]\s+', text)
        character_sentences = [s for s in sentences if character_name in s]
        
        profile = CharacterProfile(
            name=character_name,
            core_identity=[],
            personality_traits=[],
            physical_attributes=[],
            relationships={},
            motivations=[],
            conflicts=[],
            skills_abilities=[],
            significant_events=[],
            narrative_role="",
            character_arc=[]
        )
        
        # Extract using pattern matching
        self._extract_patterns(character_sentences, profile)
        
        # Use AI for deeper semantic analysis if available
        if self.client:
            self._ai_analysis(text, character_name, profile)
        else:
            self._rule_based_analysis(character_sentences, profile)
        
        return profile
    
    def _extract_patterns(self, sentences: List[str], profile: CharacterProfile):
        """Extract character information using regex patterns"""
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Physical attributes
            for pattern in self.trait_patterns['physical']:
                matches = re.findall(pattern, sentence_lower)
                profile.physical_attributes.extend([f"{match} {sentence}" for match in matches])
            
            # Personality traits
            for pattern in self.trait_patterns['personality']:
                matches = re.findall(pattern, sentence_lower)
                profile.personality_traits.extend([f"{match} {sentence}" for match in matches])
            
            # Relationships
            for pattern in self.trait_patterns['relationships']:
                matches = re.findall(pattern, sentence_lower)
                for match in matches:
                    # Try to identify who the relationship is with
                    other_char = self._find_relationship_target(sentence, profile.name)
                    if other_char:
                        profile.relationships[other_char] = match
            
            # Narrative elements
            for category, patterns in self.narrative_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, sentence_lower):
                        if category == 'conflict':
                            profile.conflicts.append(sentence)
                        elif category == 'motivation':
                            profile.motivations.append(sentence)
                        elif category == 'change':
                            profile.character_arc.append(sentence)
    
    def _find_relationship_target(self, sentence: str, main_character: str) -> str:
        """Find who the main character has a relationship with in a sentence"""
        words = re.findall(r'\b[A-Z][a-z]{2,}\b', sentence)
        for word in words:
            if word != main_character and word not in ['The', 'This', 'That', 'Chapter']:
                return word
        return "unknown"
    
    def _ai_analysis(self, text: str, character_name: str, profile: CharacterProfile):
        """Use AI for deeper semantic character analysis"""
        
        prompt = f"""
        Analyze the character {character_name} in this text and extract meaningful insights:

        TEXT: {text}

        Provide a structured analysis focusing on:
        1. Core identity (who they fundamentally are)
        2. Personality traits (how they behave and think)
        3. Narrative role (their function in the story)
        4. Key motivations (what drives them)
        5. Internal/external conflicts
        6. Skills and abilities
        7. Significant character development moments

        Be specific and quote evidence from the text. Focus on what's truly important about this character, not every minor detail.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a literary analyst specializing in character development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            
            # Parse the AI response into structured data
            self._parse_ai_analysis(analysis, profile)
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            self._rule_based_analysis(text.split('.'), profile)
    
    def _parse_ai_analysis(self, analysis: str, profile: CharacterProfile):
        """Parse AI analysis into structured profile data"""
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify sections
            if 'core identity' in line.lower():
                current_section = 'core_identity'
            elif 'personality' in line.lower():
                current_section = 'personality_traits'
            elif 'narrative role' in line.lower():
                current_section = 'narrative_role'
            elif 'motivation' in line.lower():
                current_section = 'motivations'
            elif 'conflict' in line.lower():
                current_section = 'conflicts'
            elif 'skills' in line.lower() or 'abilities' in line.lower():
                current_section = 'skills_abilities'
            elif 'development' in line.lower() or 'arc' in line.lower():
                current_section = 'character_arc'
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                # Extract bullet points
                content = line.lstrip('-•* ').strip()
                if current_section and content:
                    getattr(profile, current_section).append(content)
    
    def _rule_based_analysis(self, sentences: List[str], profile: CharacterProfile):
        """Fallback rule-based analysis when AI is not available"""
        
        for sentence in sentences:
            if profile.name not in sentence:
                continue
                
            sentence_lower = sentence.lower()
            
            # Core identity indicators
            if any(word in sentence_lower for word in ['is', 'was', 'are', 'were']):
                if any(word in sentence_lower for word in ['artist', 'writer', 'doctor', 'teacher']):
                    profile.core_identity.append(sentence)
            
            # Skills and abilities
            if any(word in sentence_lower for word in ['paints', 'writes', 'sings', 'dances', 'fights']):
                profile.skills_abilities.append(sentence)
            
            # Narrative role inference
            if 'protagonist' in sentence_lower or 'main character' in sentence_lower:
                profile.narrative_role = "protagonist"
            elif 'antagonist' in sentence_lower:
                profile.narrative_role = "antagonist"
            elif 'mentor' in sentence_lower:
                profile.narrative_role = "mentor"
    
    def deduplicate_and_rank(self, profile: CharacterProfile) -> CharacterProfile:
        """Remove duplicates and rank insights by importance"""
        
        def deduplicate_list(items: List[str]) -> List[str]:
            seen = set()
            unique = []
            for item in items:
                # Simple deduplication based on first 50 chars
                key = item[:50].lower().strip()
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            return unique
        
        # Deduplicate all lists
        profile.core_identity = deduplicate_list(profile.core_identity)
        profile.personality_traits = deduplicate_list(profile.personality_traits)
        profile.physical_attributes = deduplicate_list(profile.physical_attributes)
        profile.motivations = deduplicate_list(profile.motivations)
        profile.conflicts = deduplicate_list(profile.conflicts)
        profile.skills_abilities = deduplicate_list(profile.skills_abilities)
        profile.significant_events = deduplicate_list(profile.significant_events)
        profile.character_arc = deduplicate_list(profile.character_arc)
        
        # Rank by importance (simple heuristic: longer sentences with more specific content)
        def rank_importance(items: List[str]) -> List[str]:
            return sorted(items, key=lambda x: len(x), reverse=True)[:5]  # Keep top 5
        
        profile.personality_traits = rank_importance(profile.personality_traits)
        profile.motivations = rank_importance(profile.motivations)
        profile.conflicts = rank_importance(profile.conflicts)
        
        return profile
    
    def save_character_profile(self, profile: CharacterProfile, output_dir: str):
        """Save the intelligent character profile"""
        
        os.makedirs(output_dir, exist_ok=True)
        profile_dict = {
            'name': profile.name,
            'analysis_timestamp': os.path.getmtime(__file__) if os.path.exists(__file__) else None,
            'core_identity': profile.core_identity,
            'personality_traits': profile.personality_traits,
            'physical_attributes': profile.physical_attributes,
            'relationships': profile.relationships,
            'motivations': profile.motivations,
            'conflicts': profile.conflicts,
            'skills_abilities': profile.skills_abilities,
            'significant_events': profile.significant_events,
            'narrative_role': profile.narrative_role,
            'character_arc': profile.character_arc
        }
        
        output_file = os.path.join(output_dir, f"{profile.name.lower()}_profile.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(profile_dict, f, indent=2, ensure_ascii=False)
        
        print(f"[✓] Intelligent profile saved: {output_file}")
        return output_file

# Integration function
def create_intelligent_profiles(characters_dir: str, summaries_dir: str, output_dir: str):
    """Create intelligent profiles for all characters"""
    
    profiler = IntelligentCharacterProfiler()
    
    # Get all character files
    character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
    
    for char_file in character_files:
        char_path = os.path.join(characters_dir, char_file)
        
        with open(char_path, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
        
        character_name = char_data.get('name', char_file.replace('.json', ''))
        
        # Collect all text about this character
        all_text = []
        
        # Add established facts
        all_text.extend(char_data.get('established_facts', []))
        
        # Add observed behaviors
        for behavior in char_data.get('observed_behaviors', []):
            if isinstance(behavior, dict):
                all_text.append(behavior.get('behavior', ''))
            else:
                all_text.append(str(behavior))
        
        # Combine all text
        combined_text = ' '.join(all_text)
        
        if combined_text.strip():
            print(f"\n🔍 Analyzing {character_name}...")
            
            # Extract intelligent profile
            profile = profiler.extract_character_insights(combined_text, character_name)
            profile = profiler.deduplicate_and_rank(profile)
            
            # Save profile
            profiler.save_character_profile(profile, output_dir)
        else:
            print(f"⚠️ No text found for {character_name}")

if __name__ == "__main__":
    # Test with existing data
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    characters_dir = os.path.join(data_dir, "characters")
    summaries_dir = os.path.join(data_dir, "summaries")
    profiles_dir = os.path.join(data_dir, "character_profiles")
    
    create_intelligent_profiles(characters_dir, summaries_dir, profiles_dir)
