# Narrative Engine - Editorial Intelligence Platform

## Project Complete

A sophisticated fiction editing and narrative analysis platform with AI-powered critique, character management, and editorial intelligence.

---

## Design System

### Color Palette
- **Background**: Deep graphite (#0B0F14)
- **Primary**: Electric blue (#2D5AFF)
- **Accent**: Cyan (#00D9FF)
- **Secondary Accents**: Emerald (#10B981), Amber (#F59E0B), Purple (#A855F7)
- **Gradients**: Blue-to-violet, emerald-to-cyan, amber-to-gold for premium feel

### Typography
- **Headings**: Georgia/Garamond serif fallback - elegant, literary aesthetic
- **Body**: Geist (sans-serif) - clean, readable
- **Code**: Geist Mono

### Visual Effects
- Glassmorphism with backdrop blur and semi-transparent layering
- Glow effects on primary/accent elements
- Smooth spring-physics animations (Framer Motion: stiffness 300, damping 30)
- Particle effects for premium feel
- Cursor trail with trailing glow effect
- Hover state elevation and color transitions
- Staggered entry animations for grids and lists
- Tooltip animations with AnimatePresence

### Animation Details (Framer Motion v11)
- **Metric Cards**: Scale & opacity entry, hover scale 1.05 with y-lift
- **Chapter Grid**: Staggered y-axis entry (20px offset), hover lift with scale
- **Character Cards**: Rotate entry (-2deg) + opacity, hover rotate 1deg with scale
- **Navigation Icons**: Individual stagger delay (50-100ms), icon scale/rotate on hover
- **Logo**: Spring rotation entry with continuous hover effect
- **Tooltips**: AnimatePresence for smooth fade in/out transitions

---

## Architecture

### 3-Panel Workspace Layout
1. **Left Navigation Rail** (80px fixed)
   - Logo/branding
   - 6 main navigation items with icons
   - Bottom action button
   - Tooltips on hover

2. **Center Content Area** (flexible)
   - Main editing and viewing canvas
   - Responsive to screen size
   - Scrollable with custom styling

3. **Right Intelligence Panel** (320px fixed)
   - AI insights and memory system
   - Expandable insight items
   - Character memory tracking
   - Continuity issue flagging
   - Editorial suggestions based on voice

### Background System
- Parallax background that responds to mouse movement
- Animated radial gradients for depth
- Subtle grid overlay for structure
- Multiple opacity layers for visual hierarchy

---

## Core Pages & Components

### Dashboard (`/`)
**MetricsCards Component**
- 4 animated metric cards with:
  - Animated number counters (ease-out quad easing)
  - Gradient backgrounds per metric
  - Progress bars showing target completion
  - Hover state reveals percentage

**ChapterGrid Component**
- Grid of chapter cards with:
  - Title, word count, last edited timestamp
  - Status badges (draft/reviewing/complete)
  - AI quality score with color-coded values
  - Hover states with gradient backgrounds
  - "Open" action button appears on hover

### Characters (`/characters`)
**CharacterCards**
- Character profile cards with gradient halos
- Role, traits, and appearance count
- Importance level indicators
- Hover animations with glow effects

**CharacterRelationshipGraph**
- Interactive canvas-based relationship visualization
- Node positions represent character connections
- Edge colors indicate relationship types
- Force-directed layout with physics simulation

**CharacterTimelineView**
- Chronological display of character events
- Key story moments and turning points
- Chapter references with navigation
- Vertical timeline design

### Editorial Pipeline (`/pipeline`)
**Voice Selector**
- Choose editorial voice: Friendly, Strict, Forensic
- Different feedback styles for each voice

**RadarChart (Critique Display)**
- Multi-dimensional prose quality assessment:
  - Prose Quality (70-95)
  - Pacing (65-90)
  - Character Development (75-92)
  - Dialogue Quality (70-85)
  - Emotional Impact (80-95)
  - Plot Progression (75-88)

**CritiqueSection**
- Organized feedback by category:
  - Strengths (green) - what works well
  - Weaknesses (red) - areas for improvement
  - Suggestions (amber) - specific recommendations
- Expandable items with detailed explanations

### Line Editor (`/editor`)
**SplitViewEditor**
- Original text on left, editor on right
- Resizable divider between panels
- Inline highlighting for suggested edits
- Checkbox-based suggestion acceptance
- Word count and statistics tracking
- Full-width responsive layout

### Analytics (`/analytics`)
**Stats Cards**
- Quality score trend
- Writing consistency metrics
- Session statistics
- Change indicators (up/down)

**Quality Score Chart**
- Visual representation of narrative quality over time
- Line chart tracking score progression

**Writing Insights**
- Top 3 strengths identified
- Top 3 improvement areas
- Character performance metrics
- Engagement analysis

### Settings (`/settings`)
**Editorial Voice Customization**
- Configure feedback tone and style
- Focus area selection
- Auto-save preferences

**Focus Areas**
- Toggle specific analysis categories
- Customize which aspects to emphasize

**Preferences**
- Auto-save toggle
- Theme selector
- API configuration

---

## Interactive Components

### Motion & Animation System (`lib/motion.ts`)
- **Spring Physics**: Predefined animation curves (micro, small, default, major)
- **Fade Animations**: fadeInUp, fadeInScale
- **Container Effects**: staggerContainer with staggered children
- **Glow Pulses**: Subtle pulsing glow effects
- **Shimmer Effects**: Animated background shimmer

### Particle Effect (`ParticleEffect.tsx`)
- Canvas-based particle system
- Configurable count, colors, speed, size
- Automatic regeneration of faded particles
- Perfect for background ambiance

### Cursor Glow (`CursorGlow.tsx`)
- Trailing cursor effect
- Dual-color glow (blue + cyan)
- Canvas-based for performance
- Scales based on movement speed

### Hover Glow (`HoverGlow.tsx`)
- Mouse-tracking radial gradient
- Proximity-based intensity
- Customizable glow color

### Glossy Button (`GlossyButton.tsx`)
- 4 variants: primary, secondary, accent, ghost
- 3 sizes: sm, md, lg
- Glass shine effect on hover
- Smooth transitions and active states

---

## State Management

### AppContext (`lib/context/AppContext.tsx`)
Provides global state for:
- **Characters**: Full character database with relationships
- **Chapters**: All chapter metadata and status
- **Critiques**: AI-generated feedback items
- **Selection State**: Currently selected chapter/character
- **Context Methods**: setSelectedChapter, setSelectedCharacter

### Sample Data Included
- 3 pre-populated characters (Elena, Marcus, Catherine)
- 2 sample chapters with metadata
- 3 critique examples (strength/weakness/suggestion)

---

## Navigation Structure

```
/                    Dashboard
/characters          Character management
/editor              Line-by-line editor
/pipeline            Editorial pipeline & critique
/analytics           Writing analytics & insights
/settings            User preferences & config
```

---

## UI Component Library

### Common Components
- **ParticleEffect** - Ambient particle system
- **HoverGlow** - Proximity-based glow effect
- **CursorGlow** - Mouse trail effect
- **GlossyButton** - Premium button variants

### Layout Components
- **ParallaxBackground** - Interactive background
- **LeftNavRail** - Main navigation
- **RightIntelligencePanel** - AI insights sidebar
- **WorkspaceLayout** - Main 3-panel container

### Dashboard Components
- **MetricsCards** - Animated stat cards
- **ChapterGrid** - Chapter management grid

### Character System
- **CharacterCards** - Character profiles
- **CharacterRelationshipGraph** - Relationship visualization
- **CharacterTimelineView** - Timeline display

### Critique Display
- **RadarChart** - Multi-dimensional assessment
- **CritiqueSection** - Organized feedback

### Editor
- **SplitViewEditor** - Dual-pane editor

---

## Styling & Responsive Design

### Tailwind Configuration
- Custom color variables matching dark academia theme
- Glass morphism utilities (glass-panel, glow-accent, glow-primary, glass-hover)
- Responsive grid: 1 col mobile, 2 col tablet, 3-4 col desktop

### Glassmorphism Effects
```css
.glass-panel {
  backdrop-blur-xl
  bg-card/80
  border border-border/50
}
```

### Glow Effects
```css
.glow-accent {
  shadow-lg shadow-accent/20
}

.glow-primary {
  shadow-lg shadow-primary/20
}
```

---

## Performance Optimizations

- Canvas-based effects (particles, cursor glow) for smooth 60fps
- Lazy loading of components
- CSS transitions instead of JavaScript where possible
- Requestanimationframe for smooth animations
- Optimized font loading via Next.js

---

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires CSS Grid, Flexbox, CSS Custom Properties
- Canvas API for particle and glow effects

---

## Future Enhancement Ideas

1. **Real Database Integration**: Connect to Supabase/Neon for persistent data
2. **AI Integration**: Add actual LLM critique generation
3. **Collaborative Features**: Real-time co-editing with multiplayer support
4. **Export Options**: PDF, EPUB, Word document exports
5. **Custom Themes**: User-created color scheme presets
6. **Plugin System**: Allow third-party analysis tools
7. **Version Control**: Track revision history and diffs
8. **Advanced Analytics**: Sentiment analysis, readability metrics, genre classification

---

## Files & Structure

```
/app
  /page.tsx (Dashboard)
  /characters/page.tsx
  /editor/page.tsx
  /pipeline/page.tsx
  /analytics/page.tsx
  /settings/page.tsx
  /layout.tsx (Root layout with providers)
  /globals.css (Theme & design system)

/components
  /layout
    - ParallaxBackground.tsx
    - LeftNavRail.tsx
    - RightIntelligencePanel.tsx
    - WorkspaceLayout.tsx
  
  /dashboard
    - MetricsCards.tsx
    - ChapterGrid.tsx
  
  /character-system
    - CharacterCards.tsx
    - CharacterRelationshipGraph.tsx
    - CharacterTimelineView.tsx
  
  /critique-display
    - RadarChart.tsx
    - CritiqueSection.tsx
  
  /editor
    - SplitViewEditor.tsx
  
  /common
    - ParticleEffect.tsx
    - HoverGlow.tsx
    - CursorGlow.tsx
  
  /ui
    - GlossyButton.tsx

/lib
  /context
    - AppContext.tsx
  - motion.ts (Animation definitions)
  - utils.ts (Tailwind cn utility)
```

---

## Color Reference

| Element | Color | Hex |
|---------|-------|-----|
| Background | Deep Graphite | #0B0F14 |
| Card | Dark Slate | #1A1F29 |
| Foreground | Light Gray | #E8E9EB |
| Primary | Electric Blue | #2D5AFF |
| Accent | Cyan | #00D9FF |
| Secondary | Muted Slate | #3A4557 |
| Muted | Dark Gray | #2A2F39 |
| Success | Emerald | #10B981 |
| Warning | Amber | #F59E0B |
| Destructive | Red | #DC2626 |

---

## Typography Reference

| Use | Font | Weight | Size |
|-----|------|--------|------|
| H1 | Playfair Display | 800 | 3xl |
| H2 | Playfair Display | 700 | 2xl |
| H3 | Playfair Display | 600 | xl |
| Body | Geist | 400 | base |
| Small | Geist | 400 | sm |
| Code | Geist Mono | 400 | sm |

---

**Built with Next.js 16, React 19, Tailwind CSS v4, and Framer Motion animations.**
