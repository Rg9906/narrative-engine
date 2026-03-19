'use client';

import React, { useState } from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { RadarChart } from '@/components/critique-display/RadarChart';
import { CritiqueSection } from '@/components/critique-display/CritiqueSection';
import { cn } from '@/lib/utils';

type EditorialVoice = 'friendly' | 'strict' | 'forensic';

const sampleRadarData = [
  { label: 'Prose', value: 88, color: '#2D5AFF' },
  { label: 'Pacing', value: 82, color: '#06D6D0' },
  { label: 'Character', value: 91, color: '#10B981' },
  { label: 'Theme', value: 85, color: '#F59E0B' },
  { label: 'Coherence', value: 79, color: '#A855F7' },
];

const strengths = [
  {
    id: '1',
    title: 'Compelling protagonist arc',
    severity: 'info' as const,
    description: 'Elena\'s character development is emotionally resonant',
    explanation: 'The transformation from uncertainty to agency spans multiple chapters with consistent motivation.',
    context: 'Evident in chapters 2, 5, and 8',
  },
  {
    id: '2',
    title: 'Vivid world-building',
    severity: 'info' as const,
    description: 'The setting feels immersive and well-realized',
    explanation: 'Sensory details are woven naturally into dialogue and action.',
    context: 'Particularly strong in chapters 1 and 6',
  },
];

const weaknesses = [
  {
    id: '1',
    title: 'Pacing dip in middle act',
    severity: 'warning' as const,
    description: 'Chapters 4-6 move slowly through exposition',
    explanation: 'While necessary information is conveyed, consider breaking up long passages with dialogue or action.',
    suggestion: 'Consider restructuring chapter 5 to show rather than tell the political landscape.',
    context: 'Chapter 5: 2500+ words of narrative summary',
  },
  {
    id: '2',
    title: 'Secondary character development',
    severity: 'warning' as const,
    description: 'James could use more depth and motivation',
    explanation: 'Currently feels more like a plot device than a fully realized character.',
    suggestion: 'Add a scene exploring his personal stake in the conflict.',
    context: 'Appears in chapters 4, 7, 9, 11',
  },
];

const suggestions = [
  {
    id: '1',
    title: 'Dialogue punctuation',
    severity: 'info' as const,
    description: '3 instances of missing comma after dialogue tag',
    explanation: 'Follows standard manuscript formatting guidelines.',
    suggestion: 'Line 42: Change "I can\'t," she said. to "I can\'t," she said,',
    context: 'Chapter 3, 7, 9',
  },
];

export default function PipelinePage() {
  const [selectedVoice, setSelectedVoice] = useState<EditorialVoice>('friendly');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const voiceDescriptions = {
    friendly: 'Encouraging and constructive tone',
    strict: 'Rigorous technical focus',
    forensic: 'Comprehensive deep-dive analysis',
  };

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => setIsAnalyzing(false), 2000);
  };

  return (
    <WorkspaceLayout>
      <div className="space-y-12 max-w-5xl mx-auto">
        {/* Header */}
        <PageHeader 
          title="Editorial Pipeline" 
          subtitle="AI-powered manuscript analysis and critique"
          icon="◇"
        />

        {/* Voice selector */}
        <div className="glass-panel p-6 rounded-xl">
          <h2 className="text-lg font-serif font-bold text-foreground mb-4">Editorial Voice</h2>
          <div className="flex gap-3">
            {(['friendly', 'strict', 'forensic'] as const).map((voice) => (
              <button
                key={voice}
                onClick={() => setSelectedVoice(voice)}
                className={cn(
                  'px-6 py-3 rounded-lg font-medium transition-all duration-300 flex-1',
                  selectedVoice === voice
                    ? 'glass-panel border-primary/50 text-primary'
                    : 'glass-hover text-muted-foreground hover:text-foreground'
                )}
              >
                <div className="font-semibold capitalize">{voice}</div>
                <div className="text-xs text-muted-foreground mt-1">{voiceDescriptions[voice]}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Analyze button */}
        <div className="flex justify-center">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className={cn(
              'px-8 py-4 rounded-xl font-serif font-bold text-lg',
              'transition-all duration-300',
              'relative overflow-hidden group',
              isAnalyzing
                ? 'bg-primary/30 text-primary/50 cursor-not-allowed'
                : 'bg-gradient-to-r from-primary to-accent text-white glow-primary hover:scale-105 hover:shadow-xl'
            )}
          >
            <span className="relative z-10">{isAnalyzing ? 'Analyzing...' : 'Review Text'}</span>

            {isAnalyzing && (
              <div className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/30 to-primary/0 animate-pulse" />
            )}
          </button>
        </div>

        {/* Results */}
        {!isAnalyzing && (
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* Radar chart */}
            <div className="glass-panel p-6 rounded-xl">
              <h2 className="text-lg font-serif font-bold text-foreground mb-4">Quality Metrics</h2>
              <RadarChart data={sampleRadarData} />
              <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
                {sampleRadarData.map((metric) => (
                  <div key={metric.label} className="text-center">
                    <div className="text-2xl font-bold text-foreground">{metric.value}%</div>
                    <p className="text-xs text-muted-foreground mt-1">{metric.label}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Critique sections */}
            <div className="glass-panel p-6 rounded-xl space-y-8">
              <CritiqueSection title="Strengths" icon="✓" color="success" items={strengths} />
              <CritiqueSection title="Areas to Improve" icon="⚠" color="warning" items={weaknesses} />
              <CritiqueSection title="Suggestions" icon="◆" color="info" items={suggestions} />
            </div>
          </div>
        )}
      </div>
    </WorkspaceLayout>
  );
}
