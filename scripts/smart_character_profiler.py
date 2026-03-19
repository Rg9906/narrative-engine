import re
import json
import os
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from collections import Counter

@dataclass
class CharacterTrait:
    """A specific, meaningful character trait"""
    trait_type: str  # personality, motivation, conflict, skill, relationship
    description: str
    confidence: float
    source_chapter: str
    evidence: str

class SmartCharacterProfiler:
    """Intelligent character profiling that extracts only meaningful insights"""
    
    def __init__(self):
        # Key trait indicators with context
        self.trait_indicators = {
            'personality': {
                'patterns': [
                    (r'\b(kind|gentle|warm|caring)\b', 'positive_social'),
                    (r'\b(harsh|cold|cruel|unkind)\b', 'negative_social'),
                    (r'\b(shy|timid|reserved|quiet)\b', 'introverted'),
                    (r'\b(bold|confident|outgoing|assertive)\b', 'extroverted'),
                    (r'\b(intelligent|wise|clever|smart)\b', 'intelligence'),
                    (r'\b(naive|innocent|inexperienced)\b', 'naivety'),
                    (r'\b(patient|calm|composed)\b', 'temperament'),
                    (r'\b(angry|irritable|frustrated)\b', 'temperament'),
                    (r'\b(honest|truthful|sincere)\b', 'integrity'),
                    (r'\b(deceitful|dishonest|lying)\b', 'deception')
                ],
                'weight': 0.9
            },
            'motivation': {
                'patterns': [
                    (r'\b(wants|needs|desires|wishes for)\s+(\w+)', 'desire'),
                    (r'\b(hopes|dreams|aspires to)\s+(\w+)', 'aspiration'),
                    (r'\b(goal|purpose|aim|mission)\s+is\s+(\w+)', 'purpose'),
                    (r'\b(because|since|reason is)\s+(\w+)', 'reasoning'),
                    (r'\b(to|in order to|so that)\s+(\w+)', 'intention'),
                    (r'\b(driven|motivated|compelled)\s+by\s+(\w+)', 'drive'),
                    (r'\b(must|has to|needs to)\s+(\w+)', 'obligation')
                ],
                'weight': 0.85
            },
            'conflict': {
                'patterns': [
                    (r'\b(struggle|fight|battle|conflict)\s+with\s+(\w+)', 'external_conflict'),
                    (r'\b(torn|conflicted|undecided)\s+between\s+(\w+)', 'internal_conflict'),
                    (r'\b(afraid|scared|terrified|fearful)\s+of\s+(\w+)', 'fear'),
                    (r'\b(angry|furious|enraged|outraged)\s+at\s+(\w+)', 'anger'),
                    (r'\b(worried|anxious|concerned)\s+about\s+(\w+)', 'anxiety'),
                    (r'\b(jealous|envious|resentful)\s+of\s+(\w+)', 'jealousy'),
                    (r'\b(but|however|yet|although)\s+(\w+)', 'contradiction')
                ],
                'weight': 0.9
            },
            'skills': {
                'patterns': [
                    (r'\b(paints|painting|artist|artistic)\b', 'artistic'),
                    (r'\b(draws|drawing|sketches)\b', 'artistic'),
                    (r'\b(writes|writing|author|story)\b', 'literary'),
                    (r'\b(sings|singing|music|voice)\b', 'musical'),
                    (r'\b(plays|playing|instrument)\b', 'musical'),
                    (r'\b(fights|fighting|combat|skilled)\b', 'combat'),
                    (r'\b(teaches|teaching|mentor|guides)\b', 'educational'),
                    (r'\b(heals|doctor|medical|caring)\b', 'medical'),
                    (r'\b(leads|leads|commands|authority)\b', 'leadership')
                ],
                'weight': 0.8
            },
            'relationship': {
                'patterns': [
                    (r'\b(mother|father|brother|sister|son|daughter|husband|wife)\b', 'family'),
                    (r'\b(friend|ally|companion|partner)\b', 'friendship'),
                    (r'\b(enemy|rival|opponent|antagonist)\b', 'opposition'),
                    (r'\b(lover|romantic|love|beloved)\b', 'romantic'),
                    (r'\b(mentor|teacher|guide|master)\b', 'mentorship'),
                    (r'\b(loves|adores|cherishes)\s+(\w+)', 'love'),
                    (r'\b(hates|despises|detests)\s+(\w+)', 'hatred'),
                    (r'\b(trusts|believes|relies on)\s+(\w+)', 'trust'),
                    (r'\b(betrays|deceives|lies to)\s+(\w+)', 'betrayal'),
                    (r'\b(protects|defends|guards)\s+(\w+)', 'protection')
                ],
                'weight': 0.95
            },
            'physical': {
                'patterns': [
                    (r'\b(tall|short|petite|towering)\b', 'height'),
                    (r'\b(thin|slender|slim|gaunt)\b', 'build'),
                    (r'\b(heavy|large|muscular|strong)\b', 'build'),
                    (r'\b(blond|brunette|redhead|bald|gray)\s+(hair|hair)\b', 'hair_color'),
                    (r'\b(blue|green|brown|hazel|gray)\s+eyes\b', 'eye_color'),
                    (r'\b(pale|fair|dark|tanned)\s+(skin|complexion)\b', 'complexion')
                ],
                'weight': 0.7
            }
        }
        
        # Noise patterns to filter out
        self.noise_patterns = [
            r'\b(appears in chapter|chapter summary|prologue of the)\b',
            r'\b(already mentioned|previously established|introduced)\b',
            r'\b(this|that|these|those)\s+\w+',
            r'\b(said|told|asked|answered)\s+that\s+\w+',
            r'\b(was|is|are|were)\s+(just|simply|only)\s+\w+'
        ]

    def extract_character_traits(self, text: str, character_name: str, chapter_id: str) -> List[CharacterTrait]:
        """Extract meaningful traits from character text"""
        
        # Clean text by removing noise
        clean_text = self._remove_noise(text)
        
        # Split into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]\s+', clean_text) if s.strip()]
        
        # Focus on sentences that mention the character
        character_sentences = [s for s in sentences if character_name in s]
        
        traits = []
        
        for sentence in character_sentences:
            # Skip very short sentences
            if len(sentence) < 15:
                continue
            
            # Extract traits for each category
            for category, config in self.trait_indicators.items():
                trait = self._extract_trait_from_sentence(
                    sentence, category, config, character_name, chapter_id
                )
                if trait:
                    traits.append(trait)
        
        # Remove duplicates and rank by importance
        unique_traits = self._deduplicate_and_rank(traits)
        
        return unique_traits
    
    def _remove_noise(self, text: str) -> str:
        """Remove noise patterns from text"""
        for pattern in self.noise_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text
    
    def _extract_trait_from_sentence(self, sentence: str, category: str, 
                                 config: Dict, character_name: str, chapter_id: str) -> Optional[CharacterTrait]:
        """Extract a specific trait from a sentence"""
        
        for pattern, trait_type in config['patterns']:
            if re.search(pattern, sentence, re.IGNORECASE):
                # Extract meaningful description
                description = self._create_trait_description(
                    sentence, character_name, pattern, trait_type
                )
                
                if description and len(description) > 10:
                    return CharacterTrait(
                        trait_type=category,
                        description=description,
                        confidence=config['weight'],
                        source_chapter=chapter_id,
                        evidence=sentence
                    )
        
        return None
    
    def _create_trait_description(self, sentence: str, character_name: str, 
                             pattern: str, trait_type: str) -> str:
        """Create a clean trait description"""
        # Remove character name for cleaner description
        clean_sentence = sentence.replace(character_name, '').strip()
        
        # Remove leading articles and conjunctions
        clean_sentence = re.sub(r'^(and|but|so|then|however|because)\s+', '', clean_sentence.strip())
        
        # Extract the key part with the trait
        match = re.search(pattern, clean_sentence, re.IGNORECASE)
        if match:
            # Get the matched part and some context
            start = max(0, match.start() - 20)
            end = min(len(clean_sentence), match.end() + 20)
            description = clean_sentence[start:end].strip()
            
            # Clean up punctuation and filler
            description = re.sub(r'\s+', ' ', description)
            description = description.strip('.,!?;:')
            
            return description
        
        return clean_sentence[:100]  # Fallback to first 100 chars
    
    def _deduplicate_and_rank(self, traits: List[CharacterTrait]) -> List[CharacterTrait]:
        """Remove duplicates and rank by importance"""
        
        # Group by trait type and description similarity
        unique_traits = []
        seen_descriptions = set()
        
        for trait in traits:
            # Create a key for deduplication (first 50 chars, lowercase)
            key = trait.description[:50].lower().strip()
            
            if key not in seen_descriptions:
                seen_descriptions.add(key)
                unique_traits.append(trait)
            else:
                # If we've seen this trait, boost confidence
                for existing in unique_traits:
                    if existing.description[:50].lower().strip() == key:
                        existing.confidence = min(1.0, existing.confidence + 0.1)
                        existing.evidence += f" | {trait.evidence}"
                        break
        
        # Sort by confidence and description quality
        unique_traits.sort(key=lambda x: (x.confidence, len(x.description)), reverse=True)
        
        return unique_traits
    
    def create_character_profile(self, traits: List[CharacterTrait], character_name: str) -> Dict:
        """Create a clean, meaningful character profile"""
        
        profile = {
            'name': character_name,
            'core_identity': [],
            'personality_traits': [],
            'physical_attributes': [],
            'relationships': {},
            'motivations': [],
            'conflicts': [],
            'skills_abilities': [],
            'narrative_role': '',
            'character_arc': [],
            'significant_moments': []
        }
        
        # Categorize traits
        for trait in traits:
            content = f"[{trait.source_chapter}] {trait.description}"
            
            if trait.trait_type == 'personality':
                profile['personality_traits'].append(content)
            elif trait.trait_type == 'physical':
                profile['physical_attributes'].append(content)
            elif trait.trait_type == 'relationship':
                # Extract relationship target
                target = self._extract_relationship_target(trait.description)
                if target:
                    profile['relationships'][target] = content
            elif trait.trait_type == 'motivation':
                profile['motivations'].append(content)
            elif trait.trait_type == 'conflict':
                profile['conflicts'].append(content)
            elif trait.trait_type == 'skills':
                profile['skills_abilities'].append(content)
        
        # Limit to top insights per category (keep only the best)
        for key in profile:
            if isinstance(profile[key], list) and len(profile[key]) > 3:
                # Sort by description length (longer = more detailed)
                profile[key] = sorted(profile[key], key=len, reverse=True)[:3]
        
        return profile
    
    def _extract_relationship_target(self, description: str) -> Optional[str]:
        """Extract who the relationship is with"""
        # Look for capitalized words that might be names
        words = re.findall(r'\b[A-Z][a-z]{2,}\b', description)
        for word in words:
            if word not in ['The', 'This', 'That', 'Character', 'Chapter', 'However', 'Because']:
                return word
        return None

def profile_all_characters_intelligently(characters_dir: str, output_dir: str):
    """Profile all characters with smart filtering"""
    
    profiler = SmartCharacterProfiler()
    
    # Get all character files
    character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
    
    results = {}
    
    for char_file in character_files:
        char_path = os.path.join(characters_dir, char_file)
        
        with open(char_path, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
        
        character_name = char_data.get('name', char_file.replace('.json', ''))
        
        # Collect meaningful text about this character
        meaningful_text = []
        
        # Add established facts (but filter out noise)
        for fact in char_data.get('established_facts', []):
            if not any(noise in fact.lower() for noise in ['appears in chapter', 'chapter summary', 'prologue']):
                meaningful_text.append(fact)
        
        # Add observed behaviors
        for behavior in char_data.get('observed_behaviors', []):
            if isinstance(behavior, dict):
                behavior_text = behavior.get('behavior', '')
            else:
                behavior_text = str(behavior)
            
            if behavior_text and len(behavior_text) > 20:
                meaningful_text.append(behavior_text)
        
        # Combine all meaningful text
        combined_text = ' '.join(meaningful_text)
        
        if combined_text.strip():
            print(f"\n🧠 Smart profiling {character_name}...")
            
            # Extract traits
            traits = profiler.extract_character_traits(
                combined_text, character_name, "combined"
            )
            
            # Create profile
            profile = profiler.create_character_profile(traits, character_name)
            profile['analysis_method'] = 'smart_semantic_filtering'
            profile['total_traits'] = len(traits)
            
            # Save profile
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{character_name.lower()}_smart_profile.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            print(f"[✓] Smart profile saved: {output_file}")
            print(f"    📊 Meaningful traits: {len(traits)}")
            
            # Show summary
            if profile['personality_traits']:
                print(f"    🎭 Personality: {len(profile['personality_traits'])} traits")
            if profile['motivations']:
                print(f"    🎯 Motivations: {len(profile['motivations'])} found")
            if profile['conflicts']:
                print(f"    ⚔️ Conflicts: {len(profile['conflicts'])} identified")
            if profile['relationships']:
                print(f"    👥 Relationships: {len(profile['relationships'])} found")
            
            results[character_name] = profile
        else:
            print(f"⚠️ No meaningful content found for {character_name}")
    
    return results

if __name__ == "__main__":
    # Test with existing data
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    characters_dir = os.path.join(data_dir, "characters")
    smart_profiles_dir = os.path.join(data_dir, "smart_character_profiles")
    
    profile_all_characters_intelligently(characters_dir, smart_profiles_dir)
