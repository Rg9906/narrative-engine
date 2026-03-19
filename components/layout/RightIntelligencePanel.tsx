'use client';

import React, { useState } from 'react';
import { cn } from '@/lib/utils';

interface InsightItem {
  type: 'memory' | 'inconsistency' | 'suggestion';
  title: string;
  description: string;
  context?: string;
}

const sampleInsights: InsightItem[] = [
  {
    type: 'memory',
    title: 'Character Memory',
    description: 'Elena was introduced with green eyes in Chapter 2',
    context: 'Conflicting description in Chapter 7',
  },
  {
    type: 'inconsistency',
    title: 'Continuity Issue',
    description: 'Timeline gap between scenes',
    context: '3-day jump not explained',
  },
  {
    type: 'suggestion',
    title: 'Pacing Suggestion',
    description: 'This section could benefit from more action',
    context: 'Matches editorial voice: Friendly',
  },
];

export function RightIntelligencePanel() {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getIconColor = (type: InsightItem['type']) => {
    switch (type) {
      case 'memory':
        return 'text-accent';
      case 'inconsistency':
        return 'text-destructive';
      case 'suggestion':
        return 'text-yellow-500';
      default:
        return 'text-muted-foreground';
    }
  };

  const getIconSymbol = (type: InsightItem['type']) => {
    switch (type) {
      case 'memory':
        return '◆';
      case 'inconsistency':
        return '⚠';
      case 'suggestion':
        return '✓';
      default:
        return '○';
    }
  };

  return (
    <div className="w-80 h-screen fixed right-0 top-0 glass-panel border-l rounded-none flex flex-col z-40 overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-border/50">
        <h2 className="text-lg font-serif font-bold text-foreground">Intelligence</h2>
        <p className="text-xs text-muted-foreground mt-1">AI Insights & Memory</p>
      </div>

      {/* Insights list */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-border scrollbar-track-background/50 space-y-3 p-4">
        {sampleInsights.map((insight, idx) => {
          const id = `insight-${idx}`;
          const isExpanded = expandedId === id;

          return (
            <button
              key={id}
              onClick={() => setExpandedId(isExpanded ? null : id)}
              className={cn(
                'w-full text-left p-4 rounded-lg transition-all duration-300',
                'glass-hover border border-border/30',
                isExpanded && 'ring-1 ring-primary/50'
              )}
            >
              <div className="flex items-start gap-3">
                <span className={cn('text-lg flex-shrink-0 mt-0.5', getIconColor(insight.type))}>
                  {getIconSymbol(insight.type)}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm text-foreground">{insight.title}</div>
                  <p className="text-xs text-muted-foreground mt-1">{insight.description}</p>

                  {isExpanded && insight.context && (
                    <div className="mt-3 pt-3 border-t border-border/30">
                      <p className="text-xs text-accent">{insight.context}</p>
                    </div>
                  )}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-border/50 space-y-2">
        <button className="w-full py-2 px-3 rounded-lg bg-primary/10 hover:bg-primary/20 text-primary text-sm font-medium transition-colors duration-300">
          View All
        </button>
        <button className="w-full py-2 px-3 rounded-lg border border-border text-muted-foreground hover:text-foreground text-sm font-medium transition-colors duration-300">
          Settings
        </button>
      </div>
    </div>
  );
}
