import re
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class CharacterInsight:
    """A meaningful insight about a character"""
    category: str  # personality, motivation, conflict, skill, relationship
    insight: str
    confidence: float
    source: str

class FinalCharacterProfiler:
    """Final version: extracts only truly meaningful character insights"""
    
    def __init__(self):
        # High-quality patterns for character analysis
        self.quality_patterns = {
            'personality': {
                'direct_traits': [
                    'kind', 'gentle', 'warm', 'caring', 'loving',
                    'harsh', 'cold', 'cruel', 'unkind', 'bitter',
                    'shy', 'timid', 'reserved', 'quiet', 'introverted',
                    'bold', 'confident', 'outgoing', 'assertive', 'brave',
                    'intelligent', 'wise', 'clever', 'smart', 'brilliant',
                    'naive', 'innocent', 'inexperienced', 'trusting',
                    'patient', 'calm', 'composed', 'steady', 'serene',
                    'angry', 'irritable', 'frustrated', 'impatient',
                    'honest', 'truthful', 'sincere', 'genuine',
                    'deceitful', 'dishonest', 'lying', 'manipulative'
                ],
                'behavioral_indicators': [
                    'acts', 'behaves', 'seems', 'appears', 'comes across as',
                    'has tendency to', 'always', 'never', 'typically'
                ],
                'confidence': 0.9
            },
            'motivation': {
                'desire_words': [
                    'wants', 'needs', 'desires', 'wishes', 'hopes', 'dreams of',
                    'longs for', 'craves', 'seeks', 'pursues', 'strives for'
                ],
                'purpose_words': [
                    'goal', 'purpose', 'mission', 'duty', 'responsibility',
                    'aim', 'objective', 'target', 'destination'
                ],
                'reasoning_words': [
                    'because', 'since', 'reason is', 'why', 'in order to',
                    'so that', 'to', 'for the sake of', 'driven by'
                ],
                'confidence': 0.85
            },
            'conflict': {
                'internal_conflict': [
                    'torn between', 'conflicted about', 'struggle with',
                    'undecided', 'uncertain about', 'dilemma'
                ],
                'external_conflict': [
                    'fight with', 'argue with', 'oppose', 'resist',
                    'battle against', 'compete with', 'rivalry'
                ],
                'emotional_conflict': [
                    'afraid of', 'scared of', 'terrified of', 'worried about',
                    'angry at', 'furious with', 'enraged by', 'jealous of'
                ],
                'confidence': 0.9
            },
            'skills': {
                'artistic': [
                    'paints', 'painting', 'artist', 'artistic', 'draws', 'sketches',
                    'writes', 'writing', 'author', 'storyteller', 'creates'
                ],
                'musical': [
                    'sings', 'singing', 'music', 'musical', 'voice',
                    'plays', 'instrument', 'melody', 'harmony'
                ],
                'intellectual': [
                    'teaches', 'teaching', 'mentor', 'guide', 'explains',
                    'analyzes', 'studies', 'learns', 'researches'
                ],
                'physical': [
                    'fights', 'fighting', 'combat', 'skilled', 'trained',
                    'protects', 'defends', 'guards', 'strong'
                ],
                'confidence': 0.8
            },
            'relationship': {
                'family_roles': [
                    'mother', 'father', 'brother', 'sister', 'son', 'daughter',
                    'husband', 'wife', 'uncle', 'aunt', 'cousin'
                ],
                'relationship_types': [
                    'friend', 'enemy', 'lover', 'rival', 'ally', 'partner',
                    'mentor', 'student', 'protégé', 'companion'
                ],
                'relationship_actions': [
                    'loves', 'hates', 'trusts', 'betrays', 'protects',
                    'abandons', 'supports', 'opposes', 'helps', 'harms'
                ],
                'confidence': 0.95
            }
        }
        
        # Patterns to completely ignore
        self.ignore_phrases = [
            'appears in chapter',
            'chapter summary',
            'prologue of the narrative',
            'in the prologue',
            'already mentioned',
            'previously established',
            'as we can see',
            'it is clear that',
            'the text shows'
        ]

    def extract_meaningful_insights(self, text: str, character_name: str) -> List[CharacterInsight]:
        """Extract only meaningful, high-quality insights"""
        
        # Clean text by removing ignore phrases
        clean_text = self._remove_ignore_phrases(text)
        
        # Split into sentences
        sentences = [s.strip() for s in clean_text.split('.') if s.strip()]
        
        insights = []
        
        for sentence in sentences:
            if character_name not in sentence or len(sentence) < 20:
                continue
            
            # Extract insights for each category
            insight = self._extract_personality_insight(sentence, character_name)
            if insight:
                insights.append(insight)
                continue
            
            insight = self._extract_motivation_insight(sentence, character_name)
            if insight:
                insights.append(insight)
                continue
            
            insight = self._extract_conflict_insight(sentence, character_name)
            if insight:
                insights.append(insight)
                continue
            
            insight = self._extract_skill_insight(sentence, character_name)
            if insight:
                insights.append(insight)
                continue
            
            insight = self._extract_relationship_insight(sentence, character_name)
            if insight:
                insights.append(insight)
        
        # Remove duplicates and rank
        return self._deduplicate_and_rank(insights)
    
    def _remove_ignore_phrases(self, text: str) -> str:
        """Remove phrases that indicate noise/meta commentary"""
        for phrase in self.ignore_phrases:
            text = text.replace(phrase, '')
        return text
    
    def _extract_personality_insight(self, sentence: str, character_name: str) -> Optional[CharacterInsight]:
        """Extract personality insights"""
        patterns = self.quality_patterns['personality']
        
        # Check for direct traits
        for trait in patterns['direct_traits']:
            if trait in sentence.lower():
                # Extract meaningful fragment
                insight_text = self._extract_meaningful_fragment(sentence, character_name, trait)
                if insight_text:
                    return CharacterInsight(
                        category='personality',
                        insight=f"{trait.capitalize()}: {insight_text}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        # Check for behavioral indicators
        for indicator in patterns['behavioral_indicators']:
            if indicator in sentence.lower():
                # Look for trait after indicator
                trait = self._find_trait_after_indicator(sentence, indicator)
                if trait:
                    return CharacterInsight(
                        category='personality',
                        insight=f"Behavioral: {trait}",
                        confidence=patterns['confidence'] * 0.8,
                        source=sentence
                    )
        
        return None
    
    def _extract_motivation_insight(self, sentence: str, character_name: str) -> Optional[CharacterInsight]:
        """Extract motivation insights"""
        patterns = self.quality_patterns['motivation']
        
        # Check desire words
        for desire in patterns['desire_words']:
            if desire in sentence.lower():
                object_of_desire = self._extract_object_after_word(sentence, desire)
                if object_of_desire:
                    return CharacterInsight(
                        category='motivation',
                        insight=f"Desires: {object_of_desire}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        # Check purpose words
        for purpose in patterns['purpose_words']:
            if purpose in sentence.lower():
                purpose_object = self._extract_object_after_word(sentence, purpose)
                if purpose_object:
                    return CharacterInsight(
                        category='motivation',
                        insight=f"Purpose: {purpose_object}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        return None
    
    def _extract_conflict_insight(self, sentence: str, character_name: str) -> Optional[CharacterInsight]:
        """Extract conflict insights"""
        patterns = self.quality_patterns['conflict']
        
        # Check internal conflict
        for conflict in patterns['internal_conflict']:
            if conflict in sentence.lower():
                options = self._extract_conflict_options(sentence, conflict)
                if options:
                    return CharacterInsight(
                        category='conflict',
                        insight=f"Internal conflict: {options}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        # Check emotional conflict
        for emotion in patterns['emotional_conflict']:
            if emotion in sentence.lower():
                target = self._extract_object_after_word(sentence, emotion)
                if target:
                    return CharacterInsight(
                        category='conflict',
                        insight=f"Emotional: {emotion} {target}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        return None
    
    def _extract_skill_insight(self, sentence: str, character_name: str) -> Optional[CharacterInsight]:
        """Extract skill insights"""
        patterns = self.quality_patterns['skills']
        
        for category, skills in patterns.items():
            if category == 'confidence':
                continue
                
            for skill in skills:
                if skill in sentence.lower():
                    return CharacterInsight(
                        category='skills',
                        insight=f"{category.capitalize()}: {skill}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        return None
    
    def _extract_relationship_insight(self, sentence: str, character_name: str) -> Optional[CharacterInsight]:
        """Extract relationship insights"""
        patterns = self.quality_patterns['relationship']
        
        # Check family roles
        for role in patterns['family_roles']:
            if role in sentence.lower():
                return CharacterInsight(
                    category='relationship',
                    insight=f"Family: {role}",
                    confidence=patterns['confidence'],
                    source=sentence
                )
        
        # Check relationship types
        for rel_type in patterns['relationship_types']:
            if rel_type in sentence.lower():
                target = self._extract_relationship_target(sentence)
                if target:
                    return CharacterInsight(
                        category='relationship',
                        insight=f"{rel_type.capitalize()}: {target}",
                        confidence=patterns['confidence'],
                        source=sentence
                    )
        
        return None
    
    def _extract_meaningful_fragment(self, sentence: str, character_name: str, trait: str) -> str:
        """Extract meaningful fragment around a trait"""
        # Find the trait in the sentence
        trait_index = sentence.lower().find(trait)
        if trait_index == -1:
            return ""
        
        # Extract context around the trait (50 chars total)
        start = max(0, trait_index - 20)
        end = min(len(sentence), trait_index + len(trait) + 30)
        
        fragment = sentence[start:end].strip()
        
        # Clean up
        fragment = fragment.replace(character_name, '').strip()
        fragment = re.sub(r'\s+', ' ', fragment)
        
        return fragment
    
    def _find_trait_after_indicator(self, sentence: str, indicator: str) -> Optional[str]:
        """Find trait that comes after an indicator"""
        indicator_index = sentence.lower().find(indicator)
        if indicator_index == -1:
            return None
        
        # Look for trait after indicator
        after_indicator = sentence[indicator_index + len(indicator):].strip()
        
        # Extract first meaningful word/phrase
        words = after_indicator.split()[:3]  # First 3 words
        return ' '.join(words) if words else None
    
    def _extract_object_after_word(self, sentence: str, word: str) -> Optional[str]:
        """Extract object that comes after a specific word"""
        word_index = sentence.lower().find(word)
        if word_index == -1:
            return None
        
        after_word = sentence[word_index + len(word):].strip()
        
        # Extract first meaningful phrase
        words = after_word.split()[:4]  # First 4 words
        return ' '.join(words) if words else None
    
    def _extract_conflict_options(self, sentence: str, conflict_word: str) -> Optional[str]:
        """Extract options in a conflict"""
        conflict_index = sentence.lower().find(conflict_word)
        if conflict_index == -1:
            return None
        
        after_conflict = sentence[conflict_index + len(conflict_word):].strip()
        
        # Look for "between X and Y" pattern
        if 'between' in after_conflict.lower():
            parts = after_conflict.split('between')
            if len(parts) > 1:
                options = parts[1].strip()[:50]  # First 50 chars
                return f"between {options}"
        
        return after_conflict[:50]  # First 50 chars
    
    def _extract_relationship_target(self, sentence: str) -> Optional[str]:
        """Extract who the relationship is with"""
        # Look for capitalized words that might be names
        words = re.findall(r'\b[A-Z][a-z]{2,}\b', sentence)
        for word in words:
            if word not in ['The', 'This', 'That', 'Character', 'Chapter', 'However', 'Because']:
                return word
        return None
    
    def _deduplicate_and_rank(self, insights: List[CharacterInsight]) -> List[CharacterInsight]:
        """Remove duplicates and rank by confidence"""
        # Simple deduplication by insight text
        seen = set()
        unique_insights = []
        
        for insight in insights:
            key = insight.insight[:30].lower()  # First 30 chars as key
            if key not in seen:
                seen.add(key)
                unique_insights.append(insight)
        
        # Sort by confidence
        unique_insights.sort(key=lambda x: x.confidence, reverse=True)
        
        return unique_insights
    
    def create_clean_profile(self, insights: List[CharacterInsight], character_name: str) -> Dict:
        """Create a clean, meaningful character profile"""
        
        profile = {
            'name': character_name,
            'personality_traits': [],
            'motivations': [],
            'conflicts': [],
            'skills_abilities': [],
            'relationships': [],
            'core_identity': [],
            'narrative_role': '',
            'character_arc': []
        }
        
        # Categorize insights
        for insight in insights:
            content = f"{insight.insight} [source: {insight.source[:50]}...]"
            
            if insight.category == 'personality':
                profile['personality_traits'].append(content)
            elif insight.category == 'motivation':
                profile['motivations'].append(content)
            elif insight.category == 'conflict':
                profile['conflicts'].append(content)
            elif insight.category == 'skills':
                profile['skills_abilities'].append(content)
            elif insight.category == 'relationship':
                profile['relationships'].append(content)
        
        # Limit to top insights per category
        for key in profile:
            if isinstance(profile[key], list) and len(profile[key]) > 5:
                profile[key] = profile[key][:5]  # Keep top 5
        
        return profile

def profile_characters_finally(characters_dir: str, output_dir: str):
    """Final profiling with quality filtering"""
    
    profiler = FinalCharacterProfiler()
    
    character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
    
    for char_file in character_files:
        char_path = os.path.join(characters_dir, char_file)
        
        with open(char_path, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
        
        character_name = char_data.get('name', char_file.replace('.json', ''))
        
        # Collect only meaningful text
        meaningful_texts = []
        
        # Filter established facts
        for fact in char_data.get('established_facts', []):
            if not any(phrase in fact.lower() for phrase in profiler.ignore_phrases):
                if len(fact) > 30:  # Only substantial facts
                    meaningful_texts.append(fact)
        
        # Filter observed behaviors
        for behavior in char_data.get('observed_behaviors', []):
            if isinstance(behavior, dict):
                behavior_text = behavior.get('behavior', '')
            else:
                behavior_text = str(behavior)
            
            if (len(behavior_text) > 30 and 
                not any(phrase in behavior_text.lower() for phrase in profiler.ignore_phrases)):
                meaningful_texts.append(behavior_text)
        
        combined_text = ' '.join(meaningful_texts)
        
        if combined_text.strip():
            print(f"\n🎯 Final profiling {character_name}...")
            
            # Extract insights
            insights = profiler.extract_meaningful_insights(combined_text, character_name)
            
            # Create profile
            profile = profiler.create_clean_profile(insights, character_name)
            profile['analysis_method'] = 'quality_semantic_filtering'
            profile['total_insights'] = len(insights)
            
            # Save profile
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{character_name.lower()}_final_profile.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            print(f"[✓] Final profile saved: {output_file}")
            print(f"    📊 Quality insights: {len(insights)}")
            
            # Show summary
            if profile['personality_traits']:
                print(f"    🎭 Personality: {len(profile['personality_traits'])} traits")
            if profile['motivations']:
                print(f"    🎯 Motivations: {len(profile['motivations'])} found")
            if profile['conflicts']:
                print(f"    ⚔️ Conflicts: {len(profile['conflicts'])} identified")
            if profile['skills_abilities']:
                print(f"    🛠️ Skills: {len(profile['skills_abilities'])} found")
            if profile['relationships']:
                print(f"    👥 Relationships: {len(profile['relationships'])} found")
        else:
            print(f"⚠️ No meaningful content found for {character_name}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    characters_dir = os.path.join(data_dir, "characters")
    final_profiles_dir = os.path.join(data_dir, "final_character_profiles")
    
    profile_characters_finally(characters_dir, final_profiles_dir)
