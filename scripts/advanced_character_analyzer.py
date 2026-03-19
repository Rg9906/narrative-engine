import re
import json
import os
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import hashlib

@dataclass
class CharacterInsight:
    """Represents a meaningful insight about a character"""
    category: str  # personality, motivation, conflict, etc.
    content: str
    confidence: float  # 0.0 to 1.0
    source_chapter: str
    evidence: str

class AdvancedCharacterAnalyzer:
    def __init__(self):
        # Semantic patterns for different types of insights
        self.semantic_patterns = {
            'personality': {
                'indicators': [
                    r'\b(is|was|seems|appears|acts|behaves)\s+(\w+ly|\w+)',
                    r'\b(kind|gentle|harsh|warm|cold|shy|bold|quiet|loud)\b',
                    r'\b(intelligent|wise|naive|cunning|honest|deceitful)\b',
                    r'\b(patient|impatient|calm|angry|cheerful|melancholy)\b',
                    r'\b(confident|insecure|proud|humble|arrogant)\b'
                ],
                'weight': 0.8
            },
            'physical': {
                'indicators': [
                    r'\b(tall|short|thin|heavy|slender|muscular|frail)\b',
                    r'\b(hair|eyes|face|skin)\s+(is|was|were)\s+\w+',
                    r'\b(blond|brunette|redhead|bald|gray)\s+(hair|hair)\b',
                    r'\b(blue|green|brown|hazel|gray)\s+eyes\b'
                ],
                'weight': 0.7
            },
            'relationships': {
                'indicators': [
                    r'\b(mother|father|brother|sister|son|daughter|husband|wife)\b',
                    r'\b(friend|enemy|lover|rival|ally|mentor)\b',
                    r'\b(loves|hates|trusts|betrays|protects|abandons)\b',
                    r'\b(son|daughter) of (\w+)',
                    r'\b(\w+)\'s (mother|father|brother|sister)\b'
                ],
                'weight': 0.9
            },
            'motivations': {
                'indicators': [
                    r'\b(wants|needs|desires|wishes|hopes|dreams of)\b',
                    r'\b(goal|purpose|mission|duty|responsibility)\s+(is|was)\s+\w+',
                    r'\b(because|since|reason|why)\s+(\w+)',
                    r'\b(to|in order to|so that)\s+(\w+)',
                    r'\b(driven|motivated|compelled)\s+by\s+\w+'
                ],
                'weight': 0.85
            },
            'conflicts': {
                'indicators': [
                    r'\b(struggle|fight|argue|conflict|tension)\b',
                    r'\b(afraid|scared|worried|anxious|nervous)\b',
                    r'\b(anger|rage|fury|resentment|jealousy)\b',
                    r'\b(torn|conflicted|undecided|uncertain)\b',
                    r'\b(but|however|yet|although)\s+(\w+)'
                ],
                'weight': 0.9
            },
            'skills': {
                'indicators': [
                    r'\b(paints|painting|artist|artistic)\b',
                    r'\b(writes|writing|author|literary)\b',
                    r'\b(sings|singing|musical|voice)\b',
                    r'\b(fights|fighting|skilled|trained)\b',
                    r'\b(teaches|teaching|mentor|guides)\b'
                ],
                'weight': 0.75
            },
            'role': {
                'indicators': [
                    r'\b(protagonist|main character|hero|heroine)\b',
                    r'\b(antagonist|villain|opponent)\b',
                    r'\b(mentor|guide|teacher)\b',
                    r'\b(love interest|romantic interest)\b',
                    r'\b(supporting|secondary|minor)\s+character\b'
                ],
                'weight': 0.95
            }
        }
        
        # Ignore patterns for filtering noise
        self.ignore_patterns = [
            r'\b(Appears in chapter|chapter summary|prologue of the narrative)\b',
            r'\b(This|That|The|He|She|They)\s+\w+',
            r'\b(already|appears|mentioned|introduced)\b'
        ]
        
        # Character importance indicators
        self.importance_indicators = [
            'protagonist', 'main character', 'central', 'primary',
            'antagonist', 'villain', 'opponent'
        ]

    def extract_meaningful_insights(self, text: str, character_name: str, chapter_id: str) -> List[CharacterInsight]:
        """Extract only meaningful insights about a character"""
        
        # Clean and split text
        sentences = self._clean_and_split(text, character_name)
        character_sentences = [s for s in sentences if character_name in s]
        
        insights = []
        
        for sentence in character_sentences:
            # Skip if it's just noise
            if self._is_noise(sentence):
                continue
            
            # Extract insights for each category
            for category, patterns in self.semantic_patterns.items():
                insight = self._extract_category_insight(
                    sentence, category, patterns, character_name, chapter_id
                )
                if insight:
                    insights.append(insight)
        
        # Score and rank insights
        insights = self._score_and_rank_insights(insights)
        
        return insights
    
    def _clean_and_split(self, text: str, character_name: str) -> List[str]:
        """Clean text and split into meaningful sentences"""
        # Remove common noise patterns
        for pattern in self.ignore_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)
        
        # Clean and filter
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and character_name in sentence:  # Minimum length check
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _is_noise(self, sentence: str) -> bool:
        """Check if sentence is just noise/repetition"""
        noise_indicators = [
            'appears in chapter',
            'chapter summary',
            'prologue of the narrative',
            'already mentioned',
            'previously established'
        ]
        
        sentence_lower = sentence.lower()
        return any(indicator in sentence_lower for indicator in noise_indicators)
    
    def _extract_category_insight(self, sentence: str, category: str, patterns: Dict, 
                             character_name: str, chapter_id: str) -> Optional[CharacterInsight]:
        """Extract insight for a specific category"""
        
        for pattern in patterns['indicators']:
            if re.search(pattern, sentence, re.IGNORECASE):
                # Extract the meaningful part
                insight_content = self._extract_insight_content(sentence, pattern, character_name)
                
                if insight_content and len(insight_content) > 15:  # Minimum content length
                    return CharacterInsight(
                        category=category,
                        content=insight_content,
                        confidence=patterns['weight'],
                        source_chapter=chapter_id,
                        evidence=sentence
                    )
        
        return None
    
    def _extract_insight_content(self, sentence: str, pattern: str, character_name: str) -> str:
        """Extract the meaningful content from a sentence"""
        # Remove character name for cleaner content
        content = sentence.replace(character_name, '').strip()
        
        # Remove filler words
        filler_words = ['the', 'a', 'an', 'and', 'or', 'but', 'however', 'therefore']
        words = content.split()
        content_words = [w for w in words if w.lower() not in filler_words]
        
        return ' '.join(content_words)
    
    def _score_and_rank_insights(self, insights: List[CharacterInsight]) -> List[CharacterInsight]:
        """Score and rank insights by importance"""
        
        # Remove duplicates
        unique_insights = {}
        for insight in insights:
            # Create content hash for deduplication
            content_hash = hashlib.md5(insight.content.encode()).hexdigest()
            
            if content_hash not in unique_insights:
                unique_insights[content_hash] = insight
            else:
                # Combine evidence if we've seen this before
                existing = unique_insights[content_hash]
                existing.evidence += f" | {insight.evidence}"
                # Boost confidence if seen multiple times
                existing.confidence = min(1.0, existing.confidence + 0.1)
        
        insights = list(unique_insights.values())
        
        # Sort by confidence and importance
        insights.sort(key=lambda x: (x.confidence, len(x.content)), reverse=True)
        
        return insights
    
    def create_character_profile(self, insights: List[CharacterInsight]) -> Dict:
        """Create a clean, meaningful character profile"""
        
        profile = {
            'core_identity': [],
            'personality_traits': [],
            'physical_attributes': [],
            'relationships': {},
            'motivations': [],
            'conflicts': [],
            'skills_abilities': [],
            'narrative_role': '',
            'character_arc': [],
            'key_moments': []
        }
        
        # Categorize insights
        for insight in insights:
            content = f"[{insight.source_chapter}] {insight.content}"
            
            if insight.category == 'personality':
                profile['personality_traits'].append(content)
            elif insight.category == 'physical':
                profile['physical_attributes'].append(content)
            elif insight.category == 'relationships':
                # Extract relationship target
                target = self._extract_relationship_target(insight.content)
                if target:
                    profile['relationships'][target] = insight.content
            elif insight.category == 'motivations':
                profile['motivations'].append(content)
            elif insight.category == 'conflicts':
                profile['conflicts'].append(content)
            elif insight.category == 'skills':
                profile['skills_abilities'].append(content)
            elif insight.category == 'role':
                profile['narrative_role'] = insight.content
        
        # Limit to top insights per category
        for key in profile:
            if isinstance(profile[key], list) and len(profile[key]) > 5:
                # Sort by confidence and keep top 5
                profile[key] = sorted(profile[key], key=len, reverse=True)[:5]
        
        return profile
    
    def _extract_relationship_target(self, content: str) -> Optional[str]:
        """Extract who the relationship is with"""
        # Look for capitalized words that might be names
        words = re.findall(r'\b[A-Z][a-z]{2,}\b', content)
        for word in words:
            if word not in ['The', 'This', 'That', 'Character', 'Chapter']:
                return word
        return None

def analyze_character_intelligently(characters_dir: str, summaries_dir: str, output_dir: str):
    """Analyze all characters with intelligent filtering"""
    
    analyzer = AdvancedCharacterAnalyzer()
    
    # Get all character files
    character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
    
    results = {}
    
    for char_file in character_files:
        char_path = os.path.join(characters_dir, char_file)
        
        with open(char_path, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
        
        character_name = char_data.get('name', char_file.replace('.json', ''))
        
        # Collect all text about this character
        all_text = []
        
        # Add established facts (but filter out noise)
        for fact in char_data.get('established_facts', []):
            if not analyzer._is_noise(fact):
                all_text.append(fact)
        
        # Add observed behaviors
        for behavior in char_data.get('observed_behaviors', []):
            if isinstance(behavior, dict):
                behavior_text = behavior.get('behavior', '')
            else:
                behavior_text = str(behavior)
            
            if not analyzer._is_noise(behavior_text):
                all_text.append(behavior_text)
        
        # Combine all text
        combined_text = ' '.join(all_text)
        
        if combined_text.strip():
            print(f"\n🧠 Analyzing {character_name}...")
            
            # Extract meaningful insights
            insights = analyzer.extract_meaningful_insights(
                combined_text, character_name, "combined"
            )
            
            # Create clean profile
            profile = analyzer.create_character_profile(insights)
            profile['name'] = character_name
            profile['analysis_method'] = 'advanced_semantic_filtering'
            profile['total_insights'] = len(insights)
            
            # Save profile
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{character_name.lower()}_clean_profile.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            print(f"[✓] Clean profile saved: {output_file}")
            print(f"    📊 Insights found: {len(insights)}")
            
            # Show summary
            if profile['personality_traits']:
                print(f"    🎭 Personality: {len(profile['personality_traits'])} traits")
            if profile['motivations']:
                print(f"    🎯 Motivations: {len(profile['motivations'])} found")
            if profile['conflicts']:
                print(f"    ⚔️ Conflicts: {len(profile['conflicts'])} identified")
            
            results[character_name] = profile
        else:
            print(f"⚠️ No meaningful content found for {character_name}")
    
    return results

if __name__ == "__main__":
    # Test with existing data
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    characters_dir = os.path.join(data_dir, "characters")
    summaries_dir = os.path.join(data_dir, "summaries")
    clean_profiles_dir = os.path.join(data_dir, "clean_character_profiles")
    
    analyze_character_intelligently(characters_dir, summaries_dir, clean_profiles_dir)
