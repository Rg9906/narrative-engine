'use client';

import React, { useState } from 'react';
import { cn } from '@/lib/utils';

interface CritiqueItem {
  id: string;
  title: string;
  severity: 'info' | 'warning' | 'critical';
  description: string;
  explanation?: string;
  suggestion?: string;
  context?: string;
}

interface CritiqueSectionProps {
  title: string;
  icon: string;
  color: 'success' | 'warning' | 'info';
  items: CritiqueItem[];
}

const severityColors = {
  info: 'text-cyan-500 bg-cyan-500/10',
  warning: 'text-yellow-500 bg-yellow-500/10',
  critical: 'text-red-500 bg-red-500/10',
};

export function CritiqueSection({ title, icon, color, items }: CritiqueSectionProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getHeaderColor = (color: string) => {
    switch (color) {
      case 'success':
        return 'text-emerald-500 border-emerald-500/30';
      case 'warning':
        return 'text-yellow-500 border-yellow-500/30';
      case 'info':
        return 'text-cyan-500 border-cyan-500/30';
      default:
        return 'text-muted-foreground border-border';
    }
  };

  return (
    <div className="space-y-4">
      <div className={cn('flex items-center gap-2 px-4 py-3 border-b-2', getHeaderColor(color))}>
        <span className="text-xl">{icon}</span>
        <h3 className="text-lg font-serif font-bold">{title}</h3>
        <span className="ml-auto text-sm font-medium text-muted-foreground">{items.length} items</span>
      </div>

      <div className="space-y-2">
        {items.map((item) => {
          const isExpanded = expandedId === item.id;

          return (
            <button
              key={item.id}
              onClick={() => setExpandedId(isExpanded ? null : item.id)}
              className={cn(
                'w-full text-left p-4 rounded-lg transition-all duration-300',
                'glass-hover border border-border/30',
                isExpanded && 'ring-1 ring-primary/50 border-primary/50'
              )}
            >
              <div className="flex items-start gap-3">
                <span className={cn('px-2 py-1 rounded text-xs font-medium flex-shrink-0 mt-0.5', severityColors[item.severity])}>
                  {item.severity.toUpperCase()}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-foreground">{item.title}</div>
                  <p className="text-sm text-muted-foreground mt-1">{item.description}</p>

                  {isExpanded && (
                    <div className="mt-4 space-y-3 pt-4 border-t border-border/30 animate-in fade-in duration-200">
                      {item.explanation && (
                        <div>
                          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">Explanation</p>
                          <p className="text-sm text-foreground/80">{item.explanation}</p>
                        </div>
                      )}

                      {item.suggestion && (
                        <div>
                          <p className="text-xs font-medium text-cyan-500 uppercase tracking-wider mb-1">Suggestion</p>
                          <div className="bg-cyan-500/5 border border-cyan-500/20 rounded p-3">
                            <p className="text-sm text-cyan-400">{item.suggestion}</p>
                          </div>
                        </div>
                      )}

                      {item.context && (
                        <div>
                          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">Context</p>
                          <p className="text-xs text-muted-foreground italic">{item.context}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </button>
          );
        })}

        {items.length === 0 && (
          <div className="text-center py-6 text-muted-foreground">
            <p className="text-sm">No items to review</p>
          </div>
        )}
      </div>
    </div>
  );
}
