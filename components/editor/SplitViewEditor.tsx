'use client';

import React, { useState, useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';

interface EditSuggestion {
  id: string;
  type: 'deletion' | 'addition' | 'replacement';
  original: string;
  suggested: string;
  reason: string;
  accepted: boolean;
}

const sampleText =
  'Elena walked through the dimly lit corridor. The shadows seemed to dance and move around her. She could hear the sound of footsteps echoing in the distance. Her heart was pounding in her chest. The moment had finally arrived.';

const suggestions: EditSuggestion[] = [
  {
    id: '1',
    type: 'deletion',
    original: 'The shadows seemed to dance and move around her.',
    suggested: '',
    reason: 'Clichéd personification',
    accepted: false,
  },
  {
    id: '2',
    type: 'replacement',
    original: 'She could hear the sound of footsteps',
    suggested: 'Footsteps echoed',
    reason: 'Reduce passive voice',
    accepted: false,
  },
  {
    id: '3',
    type: 'deletion',
    original: 'Her heart was pounding in her chest.',
    suggested: '',
    reason: 'Tell instead of show',
    accepted: false,
  },
];

export function SplitViewEditor() {
  const [appliedSuggestions, setAppliedSuggestions] = useState<Set<string>>(new Set());
  const [isDraggingDivider, setIsDraggingDivider] = useState(false);
  const [dividerPosition, setDividerPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDraggingDivider || !containerRef.current) return;

      const rect = containerRef.current.getBoundingClientRect();
      const newPosition = ((e.clientX - rect.left) / rect.width) * 100;

      if (newPosition > 20 && newPosition < 80) {
        setDividerPosition(newPosition);
      }
    };

    const handleMouseUp = () => {
      setIsDraggingDivider(false);
    };

    if (isDraggingDivider) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDraggingDivider]);

  const toggleSuggestion = (id: string) => {
    const newSet = new Set(appliedSuggestions);
    if (newSet.has(id)) {
      newSet.delete(id);
    } else {
      newSet.add(id);
    }
    setAppliedSuggestions(newSet);
  };

  const renderTextWithHighlights = () => {
    let segments = [{ text: sampleText, type: 'normal' as const }];

    suggestions.forEach((suggestion) => {
      segments = segments.flatMap((segment) => {
        if (segment.type !== 'normal' || !segment.text.includes(suggestion.original)) {
          return [segment];
        }

        const parts = segment.text.split(suggestion.original);
        const result = [];

        parts.forEach((part, idx) => {
          if (part) {
            result.push({ text: part, type: 'normal' as const });
          }
          if (idx < parts.length - 1) {
            result.push({
              text: suggestion.original,
              type: 'highlight' as const,
              suggestionId: suggestion.id,
            });
          }
        });

        return result;
      });
    });

    return segments.map((segment, idx) => {
      if (segment.type === 'normal') {
        return <span key={idx}>{segment.text}</span>;
      }

      const applied = appliedSuggestions.has(segment.suggestionId);
      const suggestion = suggestions.find((s) => s.id === segment.suggestionId);

      if (!suggestion) return null;

      if (suggestion.type === 'deletion') {
        return (
          <span
            key={idx}
            className={cn(
              'line-through px-1 rounded transition-colors duration-200',
              applied ? 'text-red-500 bg-red-500/20' : 'text-muted-foreground bg-red-500/5 hover:bg-red-500/15'
            )}
          >
            {segment.text}
          </span>
        );
      } else {
        return (
          <span
            key={idx}
            className={cn(
              'px-1 rounded transition-colors duration-200',
              applied ? 'text-emerald-500 bg-emerald-500/20 underline' : 'text-muted-foreground bg-emerald-500/5 hover:bg-emerald-500/15'
            )}
          >
            {segment.text}
          </span>
        );
      }
    });
  };

  return (
    <div ref={containerRef} className="h-full flex gap-4 bg-background rounded-xl overflow-hidden border border-border">
      {/* Left panel - Original text */}
      <div style={{ width: `${dividerPosition}%` }} className="overflow-y-auto p-6 border-r border-border flex flex-col">
        <div className="mb-4">
          <h3 className="text-lg font-serif font-bold text-foreground">Original</h3>
          <p className="text-xs text-muted-foreground mt-1">Chapter 3: The Approach</p>
        </div>

        <div className="flex-1 glass-panel p-4 rounded-lg leading-relaxed text-foreground/90 font-serif">
          {renderTextWithHighlights()}
        </div>

        <div className="mt-4 text-xs text-muted-foreground">
          {appliedSuggestions.size > 0 && <p>{appliedSuggestions.size} suggestion(s) applied</p>}
        </div>
      </div>

      {/* Resizable divider */}
      <div
        onMouseDown={() => setIsDraggingDivider(true)}
        className={cn(
          'w-1 cursor-col-resize transition-colors duration-200',
          'hover:bg-primary/50 bg-border',
          isDraggingDivider && 'bg-primary'
        )}
      />

      {/* Right panel - Suggestions */}
      <div style={{ width: `${100 - dividerPosition}%` }} className="overflow-y-auto p-6 flex flex-col">
        <div className="mb-4">
          <h3 className="text-lg font-serif font-bold text-foreground">Suggestions</h3>
          <p className="text-xs text-muted-foreground mt-1">{suggestions.length} edits available</p>
        </div>

        <div className="flex-1 space-y-3">
          {suggestions.map((suggestion) => {
            const isApplied = appliedSuggestions.has(suggestion.id);

            return (
              <button
                key={suggestion.id}
                onClick={() => toggleSuggestion(suggestion.id)}
                className={cn(
                  'w-full text-left p-4 rounded-lg transition-all duration-300',
                  'glass-hover border border-border/30',
                  isApplied && 'ring-1 ring-emerald-500/50 border-emerald-500/30'
                )}
              >
                <div className="flex items-start gap-3">
                  {/* Checkbox */}
                  <div
                    className={cn(
                      'w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 mt-0.5',
                      isApplied ? 'bg-emerald-500 border-emerald-500' : 'border-border'
                    )}
                  >
                    {isApplied && <span className="text-white text-sm">✓</span>}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className={cn(
                          'px-2 py-1 rounded text-xs font-medium',
                          suggestion.type === 'deletion'
                            ? 'text-red-500 bg-red-500/10'
                            : suggestion.type === 'addition'
                              ? 'text-emerald-500 bg-emerald-500/10'
                              : 'text-cyan-500 bg-cyan-500/10'
                        )}
                      >
                        {suggestion.type === 'deletion' ? 'Delete' : suggestion.type === 'addition' ? 'Add' : 'Replace'}
                      </span>
                      <span className="text-xs text-muted-foreground font-medium">{suggestion.reason}</span>
                    </div>

                    <div className="space-y-2">
                      {suggestion.original && (
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Original:</p>
                          <p className="text-sm text-foreground/80 italic opacity-75">"{suggestion.original}"</p>
                        </div>
                      )}

                      {suggestion.suggested && (
                        <div>
                          <p className="text-xs text-emerald-500 font-medium mb-1">Suggestion:</p>
                          <p className="text-sm text-emerald-400">"{suggestion.suggested}"</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
