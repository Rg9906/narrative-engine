'use client';

import React, { useState } from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { cn } from '@/lib/utils';

type EditorialVoice = 'friendly' | 'strict' | 'forensic' | 'balanced';

const voiceOptions = [
  {
    id: 'friendly',
    name: 'Friendly',
    description: 'Encouraging and constructive tone',
    icon: '◆',
    color: 'from-emerald-600 to-cyan-600',
  },
  {
    id: 'strict',
    name: 'Strict',
    description: 'Rigorous technical focus',
    icon: '⊡',
    color: 'from-red-600 to-pink-600',
  },
  {
    id: 'forensic',
    name: 'Forensic',
    description: 'Comprehensive deep-dive',
    icon: '✦',
    color: 'from-purple-600 to-blue-600',
  },
  {
    id: 'balanced',
    name: 'Balanced',
    description: 'Mix of all approaches',
    icon: '◇',
    color: 'from-amber-600 to-yellow-600',
  },
];

export default function SettingsPage() {
  const [selectedVoice, setSelectedVoice] = useState<EditorialVoice>('balanced');
  const [focusAreas, setFocusAreas] = useState(['character', 'pacing']);
  const [autoSave, setAutoSave] = useState(true);
  const [theme, setTheme] = useState('dark');

  const toggleFocusArea = (area: string) => {
    if (focusAreas.includes(area)) {
      setFocusAreas(focusAreas.filter((a) => a !== area));
    } else {
      setFocusAreas([...focusAreas, area]);
    }
  };

  const focusAreasOptions = [
    { id: 'character', label: 'Character Development' },
    { id: 'pacing', label: 'Pacing & Flow' },
    { id: 'dialogue', label: 'Dialogue Quality' },
    { id: 'worldbuilding', label: 'World Building' },
    { id: 'prose', label: 'Prose Style' },
    { id: 'formatting', label: 'Formatting' },
  ];

  return (
    <WorkspaceLayout>
      <div className="space-y-12 max-w-3xl mx-auto">
        {/* Header */}
        <PageHeader 
          title="Settings" 
          subtitle="Customize your editorial experience"
          icon="⚡"
        />

        {/* Editorial Voice Section */}
        <div className="glass-panel p-8 rounded-xl space-y-6">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Editorial Voice</h2>
            <p className="text-muted-foreground mt-2">Choose how AI feedback is delivered</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {voiceOptions.map((voice) => (
              <button
                key={voice.id}
                onClick={() => setSelectedVoice(voice.id as EditorialVoice)}
                className={cn(
                  'p-4 rounded-lg transition-all duration-300 border',
                  selectedVoice === voice.id
                    ? 'glass-panel border-primary/50 ring-2 ring-primary/30'
                    : 'glass-hover border-border/30 hover:border-border/50'
                )}
              >
                <div className={cn('w-12 h-12 rounded-lg glass-panel flex items-center justify-center text-2xl mb-3 bg-gradient-to-br', voice.color)}>
                  {voice.icon}
                </div>
                <h3 className="font-serif font-bold text-foreground text-left">{voice.name}</h3>
                <p className="text-xs text-muted-foreground mt-2 text-left">{voice.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Focus Areas */}
        <div className="glass-panel p-8 rounded-xl space-y-6">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Focus Areas</h2>
            <p className="text-muted-foreground mt-2">Select which aspects to prioritize</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {focusAreasOptions.map((area) => {
              const isSelected = focusAreas.includes(area.id);
              return (
                <button
                  key={area.id}
                  onClick={() => toggleFocusArea(area.id)}
                  className={cn(
                    'p-4 rounded-lg border transition-all duration-300 flex items-center gap-3',
                    isSelected
                      ? 'glass-panel border-primary/50 bg-primary/10'
                      : 'glass-hover border-border/30 hover:border-border/50'
                  )}
                >
                  <div
                    className={cn(
                      'w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0',
                      isSelected ? 'bg-primary border-primary' : 'border-border'
                    )}
                  >
                    {isSelected && <span className="text-white text-sm">✓</span>}
                  </div>
                  <span className="font-medium text-foreground text-left">{area.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Preferences */}
        <div className="glass-panel p-8 rounded-xl space-y-6">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Preferences</h2>
            <p className="text-muted-foreground mt-2">Configure your workspace</p>
          </div>

          <div className="space-y-4">
            {/* Auto-save toggle */}
            <div className="flex items-center justify-between p-4 rounded-lg bg-background/50 border border-border/30">
              <div>
                <p className="font-medium text-foreground">Auto-save</p>
                <p className="text-xs text-muted-foreground mt-1">Save changes automatically</p>
              </div>
              <button
                onClick={() => setAutoSave(!autoSave)}
                className={cn(
                  'w-12 h-6 rounded-full transition-all duration-300 relative',
                  autoSave ? 'bg-primary' : 'bg-border'
                )}
              >
                <div
                  className={cn('w-5 h-5 rounded-full bg-white absolute top-0.5 transition-all duration-300', autoSave ? 'right-0.5' : 'left-0.5')}
                />
              </button>
            </div>

            {/* Theme selector */}
            <div className="p-4 rounded-lg bg-background/50 border border-border/30">
              <p className="font-medium text-foreground mb-3">Theme</p>
              <div className="flex gap-3">
                {[
                  { id: 'dark', label: 'Dark' },
                  { id: 'light', label: 'Light' },
                  { id: 'auto', label: 'Auto' },
                ].map((themeOption) => (
                  <button
                    key={themeOption.id}
                    onClick={() => setTheme(themeOption.id)}
                    className={cn(
                      'px-4 py-2 rounded-lg font-medium transition-all duration-300',
                      theme === themeOption.id
                        ? 'glass-panel border-primary/50 text-primary'
                        : 'glass-hover text-muted-foreground hover:text-foreground'
                    )}
                  >
                    {themeOption.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* API Configuration */}
        <div className="glass-panel p-8 rounded-xl space-y-6">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">API Configuration</h2>
            <p className="text-muted-foreground mt-2">Advanced settings for power users</p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">API Key</label>
              <input
                type="password"
                defaultValue="sk-••••••••••••••••••••"
                className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground focus:border-primary focus:outline-none transition-colors duration-300"
              />
              <p className="text-xs text-muted-foreground mt-2">Your API key is encrypted and never shared</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Model Version</label>
              <select className="w-full px-4 py-2 rounded-lg bg-background border border-border text-foreground focus:border-primary focus:outline-none transition-colors duration-300">
                <option>Latest (GPT-4 Turbo)</option>
                <option>GPT-4</option>
                <option>GPT-3.5 Turbo</option>
              </select>
            </div>
          </div>
        </div>

        {/* Account Section */}
        <div className="glass-panel p-8 rounded-xl space-y-6">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Account</h2>
            <p className="text-muted-foreground mt-2">Manage your account</p>
          </div>

          <div className="space-y-3">
            <button className="w-full px-6 py-3 rounded-lg border border-border text-foreground hover:border-border/50 transition-all duration-300 font-medium">
              Change Password
            </button>
            <button className="w-full px-6 py-3 rounded-lg border border-border text-foreground hover:border-border/50 transition-all duration-300 font-medium">
              Download Data
            </button>
            <button className="w-full px-6 py-3 rounded-lg border border-destructive text-destructive hover:bg-destructive/10 transition-all duration-300 font-medium">
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </WorkspaceLayout>
  );
}
