'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface Character {
  id: string;
  name: string;
  role: string;
  traits: string[];
  firstAppearance: number;
  relationships: string[];
  description: string;
}

export interface Chapter {
  id: string;
  title: string;
  wordCount: number;
  lastEdited: string;
  status: 'draft' | 'reviewing' | 'complete';
  aiScore: number;
}

export interface CritiqueItem {
  id: string;
  type: 'strength' | 'weakness' | 'suggestion';
  title: string;
  description: string;
}

interface AppContextType {
  characters: Character[];
  chapters: Chapter[];
  critiques: CritiqueItem[];
  selectedChapter: Chapter | null;
  selectedCharacter: Character | null;
  setSelectedChapter: (chapter: Chapter | null) => void;
  setSelectedCharacter: (character: Character | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [characters] = useState<Character[]>([
    {
      id: '1',
      name: 'Elena Rossi',
      role: 'Protagonist',
      traits: ['Determined', 'Introspective', 'Artistic'],
      firstAppearance: 1,
      relationships: ['Marcus', 'Catherine'],
      description: 'A painter searching for truth in a world of deception.',
    },
    {
      id: '2',
      name: 'Marcus Thorne',
      role: 'Antagonist',
      traits: ['Charismatic', 'Ruthless', 'Intelligent'],
      firstAppearance: 3,
      relationships: ['Elena', 'Catherine'],
      description: 'Powerful businessman with dark secrets.',
    },
    {
      id: '3',
      name: 'Catherine Wells',
      role: 'Supporting',
      traits: ['Loyal', 'Witty', 'Protective'],
      firstAppearance: 2,
      relationships: ['Elena', 'Marcus'],
      description: 'Elena\'s best friend and confidant.',
    },
  ]);

  const [chapters] = useState<Chapter[]>([
    {
      id: '1',
      title: 'The Awakening',
      wordCount: 3840,
      lastEdited: '2 hours ago',
      status: 'reviewing',
      aiScore: 87,
    },
    {
      id: '2',
      title: 'Shadows in the Garden',
      wordCount: 4120,
      lastEdited: '1 day ago',
      status: 'complete',
      aiScore: 92,
    },
  ]);

  const [critiques] = useState<CritiqueItem[]>([
    {
      id: '1',
      type: 'strength',
      title: 'Strong Character Voice',
      description: 'Elena\'s dialogue is authentic and compelling.',
    },
    {
      id: '2',
      type: 'weakness',
      title: 'Pacing Issues',
      description: 'The middle section drags slightly.',
    },
    {
      id: '3',
      type: 'suggestion',
      title: 'Add More Sensory Detail',
      description: 'Could benefit from richer descriptive language.',
    },
  ]);

  const [selectedChapter, setSelectedChapter] = useState<Chapter | null>(null);
  const [selectedCharacter, setSelectedCharacter] = useState<Character | null>(null);

  return (
    <AppContext.Provider
      value={{
        characters,
        chapters,
        critiques,
        selectedChapter,
        selectedCharacter,
        setSelectedChapter,
        setSelectedCharacter,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
}
