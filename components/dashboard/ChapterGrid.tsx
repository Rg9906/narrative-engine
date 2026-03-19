'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Chapter {
  id: string;
  title: string;
  wordCount: number;
  lastEdited: string;
  status: 'draft' | 'reviewing' | 'complete';
  aiScore: number;
}

const sampleChapters: Chapter[] = [
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
  {
    id: '3',
    title: 'The Convergence',
    wordCount: 3650,
    lastEdited: '3 days ago',
    status: 'draft',
    aiScore: 78,
  },
  {
    id: '4',
    title: 'Echoes of Truth',
    wordCount: 4290,
    lastEdited: '5 days ago',
    status: 'complete',
    aiScore: 95,
  },
];

function ChapterCard({ chapter }: { chapter: Chapter }) {
  const [isHovered, setIsHovered] = useState(false);

  const getStatusColor = (status: Chapter['status']) => {
    switch (status) {
      case 'draft':
        return 'text-muted-foreground bg-muted/20';
      case 'reviewing':
        return 'text-yellow-500 bg-yellow-500/10';
      case 'complete':
        return 'text-emerald-500 bg-emerald-500/10';
      default:
        return 'text-muted-foreground bg-muted/20';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-500';
    if (score >= 80) return 'text-cyan-500';
    if (score >= 70) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      whileHover={{ scale: 1.02, y: -5 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={cn(
        'glass-panel p-6 rounded-xl group cursor-pointer',
        'relative overflow-hidden',
        'glow-primary border border-border/30 hover:border-primary/50'
      )}
    >
      {/* Animated gradient background on hover */}
      <div
        className={cn(
          'absolute inset-0 opacity-0 group-hover:opacity-5 transition-opacity duration-300',
          'bg-gradient-to-br from-primary to-transparent'
        )}
      />

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <h3 className="text-xl font-serif font-bold text-foreground group-hover:text-primary transition-colors duration-300 truncate">
              {chapter.title}
            </h3>
            <p className="text-sm text-muted-foreground mt-1">Chapter {chapter.id}</p>
          </div>

          <div
            className={cn(
              'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap ml-2',
              getStatusColor(chapter.status)
            )}
          >
            {chapter.status.charAt(0).toUpperCase() + chapter.status.slice(1)}
          </div>
        </div>

        {/* Content */}
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">{chapter.wordCount.toLocaleString()} words</span>
            <span className={cn('font-medium', getScoreColor(chapter.aiScore))}>
              AI Score: {chapter.aiScore}%
            </span>
          </div>

          {isHovered && (
            <div className="h-1.5 bg-border rounded-full overflow-hidden animate-in fade-in duration-300">
              <div
                className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-500"
                style={{ width: `${chapter.aiScore}%` }}
              />
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-border/30">
          <span className="text-xs text-muted-foreground">Last edited {chapter.lastEdited}</span>
          {isHovered && (
            <button className="text-xs font-medium text-accent hover:text-primary transition-colors duration-300 animate-in fade-in">
              Open →
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export function ChapterGrid() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.1,
      },
    },
  };

  return (
    <motion.div 
      className="grid grid-cols-1 md:grid-cols-2 gap-4"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {sampleChapters.map((chapter) => (
        <ChapterCard key={chapter.id} chapter={chapter} />
      ))}
    </motion.div>
  );
}
