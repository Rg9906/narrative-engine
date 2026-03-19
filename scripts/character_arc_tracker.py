import json
import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from openai import OpenAI

@dataclass
class CharacterPhase:
    """A phase/stage in a character's development"""
    phase_name: str
    chapter_start: str
    description: str
    emotional_state: str
    motivations: List[str]
    behaviors: List[str]
    triggers: List[str]
    confidence: float = 0.0
    chapter_end: Optional[str] = None

@dataclass
class CharacterAction:
    """An action taken by a character in a chapter"""
    chapter: str
    action: str
    emotional_tone: str  # "joyful", "angry", "somber", "neutral"
    context: str
    confidence: float = 0.0

@dataclass
class ConsistencyAlert:
    """Alert when character action doesn't match their current phase"""
    character: str
    chapter: str
    action: str
    current_phase: str
    expected_behavior: str
    actual_behavior: str
    severity: str  # "minor", "moderate", "major"
    explanation: str
    confidence: float

class CharacterArcTracker:
    """Advanced character arc tracking with thematic consistency checking"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key) if api_key else None
        # Get the correct data directory path
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(current_dir)
        self.data_dir = os.path.join(project_root, "data")
        self.arc_dir = os.path.join(self.data_dir, "character_arcs")
        self.phases_dir = os.path.join(self.data_dir, "character_phases")
        
        os.makedirs(self.arc_dir, exist_ok=True)
        os.makedirs(self.phases_dir, exist_ok=True)
        
        # Character arc patterns
        self.arc_indicators = {
            'life_events': [
                'death', 'died', 'killed', 'accident', 'tragedy', 'loss',
                'birth', 'born', 'new', 'discovery', 'revelation',
                'betrayal', 'betrayed', 'abandoned', 'left',
                'success', 'achieved', 'won', 'victory', 'triumph',
                'failure', 'lost', 'defeated', 'humiliation'
            ],
            'emotional_states': [
                'grieving', 'mourning', 'sorrowful', 'heartbroken',
                'joyful', 'happy', 'celebrating', 'triumphant',
                'angry', 'furious', 'enraged', 'resentful',
                'hopeful', 'optimistic', 'determined', 'motivated',
                'isolated', 'withdrawn', 'lonely', 'reclusive',
                'rebellious', 'defiant', 'resistant', 'oppositional'
            ],
            'behavioral_patterns': [
                'joking', 'laughing', 'celebrating', 'partying',
                'crying', 'weeping', 'sobbing', 'mourning',
                'fighting', 'arguing', 'conflicting', 'struggling',
                'withdrawing', 'hiding', 'avoiding', 'isolating',
                'helping', 'protecting', 'supporting', 'caring'
            ]
        }

    def analyze_character_arc_development(self, character_name: str, 
                                        chapter_texts: Dict[str, str]) -> List[CharacterPhase]:
        """Analyze character's arc development across chapters"""
        
        phases = []
        current_phase = None
        
        # Sort chapters by number
        sorted_chapters = sorted(chapter_texts.keys(), 
                              key=lambda x: int(x.replace('chapter_', '')))
        
        for chapter_id in sorted_chapters:
            text = chapter_texts[chapter_id]
            
            # Analyze this chapter for character development
            phase_analysis = self._analyze_chapter_for_phase_change(
                character_name, chapter_id, text, current_phase
            )
            
            if phase_analysis['phase_changed']:
                # Save previous phase if it exists
                if current_phase:
                    current_phase.chapter_end = chapter_id
                    phases.append(current_phase)
                
                # Create new phase
                new_phase = CharacterPhase(
                    phase_name=phase_analysis['phase_name'],
                    chapter_start=chapter_id,
                    description=phase_analysis['description'],
                    emotional_state=phase_analysis['emotional_state'],
                    motivations=phase_analysis['motivations'],
                    behaviors=phase_analysis['behaviors'],
                    triggers=phase_analysis['triggers'],
                    confidence=phase_analysis['confidence']
                )
                current_phase = new_phase
        
        # Don't forget the last phase
        if current_phase:
            phases.append(current_phase)
        
        return phases
    
    def _analyze_chapter_for_phase_change(self, character_name: str, chapter_id: str, 
                                        text: str, current_phase: Optional[CharacterPhase]) -> Dict:
        """Analyze a chapter to detect character phase changes"""
        
        if self.client:
            return self._llm_phase_analysis(character_name, chapter_id, text, current_phase)
        else:
            return self._rule_based_phase_analysis(character_name, chapter_id, text, current_phase)
    
    def _llm_phase_analysis(self, character_name: str, chapter_id: str, text: str, 
                          current_phase: Optional[CharacterPhase]) -> Dict:
        """Use LLM to analyze character phase changes"""
        
        current_state = ""
        if current_phase:
            current_state = f"""
            Current phase: {current_phase.phase_name}
            Emotional state: {current_phase.emotional_state}
            Description: {current_phase.description}
            """
        
        prompt = f"""
        Analyze the character {character_name} in this chapter for significant developmental changes.
        
        {current_state}
        
        Chapter text: {text[:2000]}  # Limit to first 2000 chars
        
        Look for:
        1. Major life events (death, loss, betrayal, success, etc.)
        2. Significant emotional state changes
        3. New motivations or changed priorities
        4. Behavioral pattern changes
        5. Turning points in character development
        
        If there's a significant change from the current state, identify:
        - New phase name (e.g., "grieving", "rebellious", "transformed", "hopeful")
        - Emotional state
        - Key triggers/events
        - New motivations
        - Changed behaviors
        
        If no significant change, indicate "no change".
        
        Respond in JSON format:
        {{
            "phase_changed": true/false,
            "phase_name": "new_phase_name",
            "emotional_state": "emotional_state",
            "description": "brief description of what changed",
            "triggers": ["trigger1", "trigger2"],
            "motivations": ["motivation1", "motivation2"],
            "behaviors": ["behavior1", "behavior2"],
            "confidence": 0.0-1.0,
            "explanation": "why this change occurred"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a literary analyst specializing in character development and narrative arcs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return self._rule_based_phase_analysis(character_name, chapter_id, text, current_phase)
    
    def _rule_based_phase_analysis(self, character_name: str, chapter_id: str, 
                                 text: str, current_phase: Optional[CharacterPhase]) -> Dict:
        """Rule-based analysis when LLM is not available"""
        
        # Look for major life events
        life_events = []
        for event in self.arc_indicators['life_events']:
            if event in text.lower():
                # Find context around the event
                event_context = self._extract_event_context(text, event, character_name)
                if event_context:
                    life_events.append((event, event_context))
        
        # Look for emotional state changes
        emotional_states = []
        for state in self.arc_indicators['emotional_states']:
            if state in text.lower():
                emotional_states.append(state)
        
        # Determine if phase changed
        phase_changed = False
        new_phase = current_phase.phase_name if current_phase else "unknown"
        emotional_state = current_phase.emotional_state if current_phase else "neutral"
        
        if life_events:
            phase_changed = True
            
            # Determine new phase based on events
            if any(event in ['death', 'died', 'killed', 'accident', 'tragedy', 'loss'] for event, _ in life_events):
                new_phase = "grieving"
                emotional_state = "sorrowful"
            elif any(event in ['betrayal', 'betrayed', 'abandoned'] for event, _ in life_events):
                new_phase = "betrayed"
                emotional_state = "angry"
            elif any(event in ['success', 'achieved', 'won', 'victory'] for event, _ in life_events):
                new_phase = "triumphant"
                emotional_state = "joyful"
        
        return {
            "phase_changed": phase_changed,
            "phase_name": new_phase,
            "emotional_state": emotional_state,
            "description": f"Phase change detected due to: {[event for event, _ in life_events]}",
            "triggers": [event for event, _ in life_events],
            "motivations": [],
            "behaviors": [],
            "confidence": 0.7 if phase_changed else 0.0,
            "explanation": "Rule-based detection of life events"
        }
    
    def _extract_event_context(self, text: str, event: str, character_name: str) -> Optional[str]:
        """Extract context around a specific event"""
        sentences = text.split('.')
        for sentence in sentences:
            if character_name in sentence and event in sentence.lower():
                return sentence.strip()
        return None
    
    def extract_character_actions(self, character_name: str, chapter_id: str, text: str) -> List[CharacterAction]:
        """Extract all actions performed by a character in a chapter"""
        
        actions = []
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        for sentence in sentences:
            if character_name in sentence:
                # Extract action and emotional tone
                action_analysis = self._analyze_action_emotion(sentence, character_name)
                if action_analysis:
                    actions.append(CharacterAction(
                        chapter=chapter_id,
                        action=action_analysis['action'],
                        emotional_tone=action_analysis['emotional_tone'],
                        context=sentence,
                        confidence=action_analysis['confidence']
                    ))
        
        return actions
    
    def _analyze_action_emotion(self, sentence: str, character_name: str) -> Optional[Dict]:
        """Analyze the emotional tone of a character's action"""
        
        if self.client:
            return self._llm_action_analysis(sentence, character_name)
        else:
            return self._rule_based_action_analysis(sentence, character_name)
    
    def _llm_action_analysis(self, sentence: str, character_name: str) -> Optional[Dict]:
        """Use LLM to analyze action emotional tone"""
        
        prompt = f"""
        Analyze the emotional tone of this character action:
        
        Character: {character_name}
        Action: {sentence}
        
        Identify:
        1. The specific action taken
        2. The emotional tone (joyful, angry, somber, neutral, etc.)
        3. Confidence in this analysis (0.0-1.0)
        
        Respond in JSON:
        {{
            "action": "specific action",
            "emotional_tone": "emotional_tone",
            "confidence": 0.0-1.0
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are analyzing character actions and emotions in literary text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return self._rule_based_action_analysis(sentence, character_name)
    
    def _rule_based_action_analysis(self, sentence: str, character_name: str) -> Optional[Dict]:
        """Rule-based action analysis"""
        
        # Look for emotional indicators
        emotional_tone = "neutral"
        confidence = 0.6
        
        # Extract action (remove character name)
        action = sentence.replace(character_name, '').strip()
        
        # Check for emotional words
        if any(word in sentence.lower() for word in ['laugh', 'joke', 'smile', 'celebrate']):
            emotional_tone = "joyful"
            confidence = 0.8
        elif any(word in sentence.lower() for word in ['cry', 'weep', 'sob', 'mourn']):
            emotional_tone = "somber"
            confidence = 0.8
        elif any(word in sentence.lower() for word in ['angry', 'fury', 'rage', 'shout']):
            emotional_tone = "angry"
            confidence = 0.8
        elif any(word in sentence.lower() for word in ['withdraw', 'hide', 'avoid', 'silent']):
            emotional_tone = "withdrawn"
            confidence = 0.7
        
        return {
            "action": action,
            "emotional_tone": emotional_tone,
            "confidence": confidence
        }
    
    def check_thematic_consistency(self, character_name: str, phases: List[CharacterPhase], 
                                 actions: List[CharacterAction]) -> List[ConsistencyAlert]:
        """Check if character actions are consistent with their current phase"""
        
        alerts = []
        
        for action in actions:
            # Find current phase for this action's chapter
            current_phase = self._get_current_phase(action.chapter, phases)
            
            if not current_phase:
                continue
            
            # Check consistency
            consistency_check = self._check_action_phase_consistency(action, current_phase)
            
            if consistency_check['is_inconsistent']:
                alert = ConsistencyAlert(
                    character=character_name,
                    chapter=action.chapter,
                    action=action.action,
                    current_phase=current_phase.phase_name,
                    expected_behavior=consistency_check['expected'],
                    actual_behavior=action.emotional_tone,
                    severity=consistency_check['severity'],
                    explanation=consistency_check['explanation'],
                    confidence=min(action.confidence, current_phase.confidence)
                )
                alerts.append(alert)
        
        return alerts
    
    def _get_current_phase(self, chapter_id: str, phases: List[CharacterPhase]) -> Optional[CharacterPhase]:
        """Get the character's current phase for a given chapter"""
        
        chapter_num = int(chapter_id.replace('chapter_', ''))
        
        for phase in phases:
            phase_start = int(phase.chapter_start.replace('chapter_', ''))
            phase_end = int(phase.chapter_end.replace('chapter_', '')) if phase.chapter_end else float('inf')
            
            if phase_start <= chapter_num <= phase_end:
                return phase
        
        return None
    
    def _check_action_phase_consistency(self, action: CharacterAction, 
                                       phase: CharacterPhase) -> Dict:
        """Check if an action is consistent with the character's current phase"""
        
        # Define consistency rules
        consistency_rules = {
            'sorrowful': {
                'inappropriate': ['joyful', 'celebrating', 'joking'],
                'expected': ['somber', 'sad', 'withdrawn', 'neutral', 'angry'],
                'severity': 'major'
            },
            'grieving': {
                'inappropriate': ['joyful', 'celebrating', 'joking'],
                'expected': ['somber', 'sad', 'withdrawn', 'neutral', 'angry'],
                'severity': 'major'
            },
            'angry': {
                'inappropriate': ['joyful', 'celebrating', 'joking'],
                'expected': ['angry', 'frustrated', 'intense', 'somber'],
                'severity': 'moderate'
            },
            'isolated': {
                'inappropriate': ['celebrating', 'socializing', 'joking'],
                'expected': ['withdrawn', 'quiet', 'somber', 'neutral'],
                'severity': 'moderate'
            },
            'hopeful': {
                'inappropriate': ['despair', 'hopeless'],
                'expected': ['optimistic', 'determined', 'positive'],
                'severity': 'minor'
            }
        }
        
        phase_emotion = phase.emotional_state.lower()
        action_emotion = action.emotional_tone.lower()
        
        # Check if there's a rule for this phase
        if phase_emotion in consistency_rules:
            rules = consistency_rules[phase_emotion]
            
            # Check for inappropriate emotions
            for inappropriate in rules['inappropriate']:
                if inappropriate in action_emotion:
                    return {
                        'is_inconsistent': True,
                        'expected': f"Should be {rules['expected'][0]} given {phase.phase_name} phase",
                        'severity': rules['severity'],
                        'explanation': f"Character in {phase.phase_name} phase should not be {action.emotional_tone}"
                    }
        
        return {
            'is_inconsistent': False,
            'expected': action.emotional_tone,
            'severity': 'none',
            'explanation': "Action is consistent with current phase"
        }
    
    def save_character_arc(self, character_name: str, phases: List[CharacterPhase]):
        """Save character arc data"""
        
        arc_data = {
            'character': character_name,
            'analysis_date': datetime.now().isoformat(),
            'phases': [asdict(phase) for phase in phases],
            'total_phases': len(phases)
        }
        
        arc_file = os.path.join(self.arc_dir, f"{character_name.lower()}_arc.json")
        with open(arc_file, 'w', encoding='utf-8') as f:
            json.dump(arc_data, f, indent=2, ensure_ascii=False)
    
    def save_consistency_alerts(self, character_name: str, alerts: List[ConsistencyAlert]):
        """Save consistency alerts"""
        
        alerts_data = {
            'character': character_name,
            'analysis_date': datetime.now().isoformat(),
            'alerts': [asdict(alert) for alert in alerts],
            'total_alerts': len(alerts),
            'severity_summary': {
                'major': len([a for a in alerts if a.severity == 'major']),
                'moderate': len([a for a in alerts if a.severity == 'moderate']),
                'minor': len([a for a in alerts if a.severity == 'minor'])
            }
        }
        
        alerts_file = os.path.join(self.arc_dir, f"{character_name.lower()}_alerts.json")
        with open(alerts_file, 'w', encoding='utf-8') as f:
            json.dump(alerts_data, f, indent=2, ensure_ascii=False)

# Integration function
def analyze_character_arcs_for_all_characters(characters_dir: str, chapters_dir: str, 
                                             api_key: str = None):
    """Analyze character arcs for all characters"""
    
    tracker = CharacterArcTracker(api_key)
    
    # Load all chapters
    chapter_texts = {}
    for chapter_file in os.listdir(chapters_dir):
        if chapter_file.endswith('.txt'):
            chapter_path = os.path.join(chapters_dir, chapter_file)
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_texts[chapter_file.replace('.txt', '')] = f.read()
    
    # Process each character
    character_files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
    
    for char_file in character_files:
        char_path = os.path.join(characters_dir, char_file)
        
        with open(char_path, 'r', encoding='utf-8') as f:
            char_data = json.load(f)
        
        character_name = char_data.get('name', char_file.replace('.json', ''))
        
        print(f"\n🎭 Analyzing character arc for {character_name}...")
        
        # Analyze arc development
        phases = tracker.analyze_character_arc_development(character_name, chapter_texts)
        
        # Extract actions from all chapters
        all_actions = []
        for chapter_id, text in chapter_texts.items():
            actions = tracker.extract_character_actions(character_name, chapter_id, text)
            all_actions.extend(actions)
        
        # Check consistency
        alerts = tracker.check_thematic_consistency(character_name, phases, all_actions)
        
        # Save results
        tracker.save_character_arc(character_name, phases)
        tracker.save_consistency_alerts(character_name, alerts)
        
        print(f"[✓] Arc analysis complete for {character_name}")
        print(f"    📊 Phases detected: {len(phases)}")
        print(f"    ⚠️ Consistency alerts: {len(alerts)}")
        
        if alerts:
            severity_summary = {}
            for alert in alerts:
                severity_summary[alert.severity] = severity_summary.get(alert.severity, 0) + 1
            
            for severity, count in severity_summary.items():
                print(f"    🚨 {severity.capitalize()}: {count}")

if __name__ == "__main__":
    # Test the system
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    characters_dir = os.path.join(data_dir, "characters")
    chapters_dir = os.path.join(data_dir, "chapters")
    
    # Run analysis (add your API key for LLM analysis)
    analyze_character_arcs_for_all_characters(characters_dir, chapters_dir)
