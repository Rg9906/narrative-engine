'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Character {
  id: string;
  name: string;
  role: string;
  appearances: number;
  importance: 'major' | 'supporting' | 'minor';
  traits: string[];
  color: string;
}

const characters: Character[] = [
  {
    id: '1',
    name: 'Elena Voss',
    role: 'Protagonist',
    appearances: 42,
    importance: 'major',
    traits: ['Determined', 'Mysterious', 'Strategic'],
    color: 'from-cyan-500 to-blue-600',
  },
  {
    id: '2',
    name: 'Marcus Gray',
    role: 'Antagonist',
    appearances: 28,
    importance: 'major',
    traits: ['Charming', 'Ruthless', 'Intelligent'],
    color: 'from-red-500 to-pink-600',
  },
  {
    id: '3',
    name: 'Sophia Chen',
    role: 'Mentor',
    appearances: 18,
    importance: 'supporting',
    traits: ['Wise', 'Compassionate', 'Evasive'],
    color: 'from-emerald-500 to-green-600',
  },
  {
    id: '4',
    name: 'James Whitmore',
    role: 'Ally',
    appearances: 12,
    importance: 'supporting',
    traits: ['Loyal', 'Humorous', 'Perceptive'],
    color: 'from-amber-500 to-yellow-600',
  },
];

function CharacterCard({ character }: { character: Character }) {
  const [isHovered, setIsHovered] = useState(false);

  const getImportanceColor = (importance: Character['importance']) => {
    switch (importance) {
      case 'major':
        return 'text-red-500 bg-red-500/10';
      case 'supporting':
        return 'text-yellow-500 bg-yellow-500/10';
      case 'minor':
        return 'text-muted-foreground bg-muted/20';
      default:
        return 'text-muted-foreground bg-muted/20';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, rotate: -2 }}
      animate={{ opacity: 1, y: 0, rotate: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      whileHover={{ scale: 1.05, rotate: 1, y: -5 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={cn(
        'glass-panel p-6 rounded-xl group cursor-pointer',
        'relative overflow-hidden',
        'border border-border/30 hover:border-accent/50'
      )}
    >
      {/* Portrait placeholder with gradient halo */}
      <div className="relative mb-4">
        <div
          className={cn(
            'w-full aspect-square rounded-lg',
            'bg-gradient-to-br',
            character.color,
            'opacity-20 group-hover:opacity-30 transition-opacity duration-300',
            'flex items-center justify-center'
          )}
        >
          <div className="text-6xl opacity-50">◆</div>
        </div>

        {/* Halo glow effect on hover */}
        {isHovered && (
          <div
            className={cn(
              'absolute inset-0 rounded-lg blur-xl opacity-20 animate-pulse',
              'bg-gradient-to-br',
              character.color
            )}
          />
        )}
      </div>

      {/* Character info */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-serif font-bold text-foreground group-hover:text-accent transition-colors duration-300">
            {character.name}
          </h3>
          <p className="text-sm text-muted-foreground">{character.role}</p>
        </div>

        {/* Importance badge */}
        <div
          className={cn('inline-block px-2.5 py-1 rounded-lg text-xs font-medium', getImportanceColor(character.importance))}
        >
          {character.importance.charAt(0).toUpperCase() + character.importance.slice(1)}
        </div>

        {/* Traits */}
        {isHovered && (
          <div className="flex flex-wrap gap-1 animate-in fade-in duration-200">
            {character.traits.map((trait) => (
              <span key={trait} className="px-2 py-1 rounded-md bg-primary/10 text-xs text-primary font-medium">
                {trait}
              </span>
            ))}
          </div>
        )}

        {/* Appearance count */}
        <div className="pt-2 border-t border-border/30 flex items-center justify-between">
          <span className="text-xs text-muted-foreground">Appearances</span>
          <span className="text-sm font-bold text-accent">{character.appearances}</span>
        </div>
      </div>
    </motion.div>
  );
}

export function CharacterCards() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.2,
      },
    },
  };

  return (
    <motion.div 
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {characters.map((character) => (
        <CharacterCard key={character.id} character={character} />
      ))}
    </motion.div>
  );
}
