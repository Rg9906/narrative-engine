'use client';

import React, { useState } from 'react';
import { cn } from '@/lib/utils';

interface TimelineEvent {
  chapter: number;
  title: string;
  character: string;
  description: string;
  color: string;
}

const events: TimelineEvent[] = [
  {
    chapter: 1,
    title: 'Elena Awakens',
    character: 'Elena',
    description: 'Discovery of hidden powers',
    color: '#06D6D0',
  },
  {
    chapter: 3,
    title: 'First Confrontation',
    character: 'Elena',
    description: 'Meets Marcus for the first time',
    color: '#EF4444',
  },
  {
    chapter: 5,
    title: 'Sophia Appears',
    character: 'Sophia',
    description: 'Mentorship begins',
    color: '#10B981',
  },
  {
    chapter: 7,
    title: 'The Alliance',
    character: 'James',
    description: 'James joins the cause',
    color: '#F59E0B',
  },
  {
    chapter: 9,
    title: 'Betrayal',
    character: 'Marcus',
    description: 'Marcus reveals his true plans',
    color: '#EF4444',
  },
  {
    chapter: 11,
    title: 'The Final Battle',
    character: 'Elena',
    description: 'Everything comes to a head',
    color: '#06D6D0',
  },
];

interface TimelineMarkerProps {
  event: TimelineEvent;
  isHovered: boolean;
  onHover: (id: number | null) => void;
}

function TimelineMarker({ event, isHovered, onHover }: TimelineMarkerProps) {
  return (
    <div
      key={event.chapter}
      onMouseEnter={() => onHover(event.chapter)}
      onMouseLeave={() => onHover(null)}
      className="flex flex-col items-center relative"
    >
      {/* Glow effect */}
      <div
        className={cn(
          'absolute top-0 w-8 h-8 rounded-full blur-lg transition-all duration-300',
          isHovered ? 'scale-150 opacity-60' : 'scale-100 opacity-30'
        )}
        style={{ backgroundColor: event.color }}
      />

      {/* Marker circle */}
      <button
        className={cn(
          'relative w-4 h-4 rounded-full border-2 transition-all duration-300',
          'hover:scale-150 z-10',
          isHovered ? 'border-white scale-125' : 'border-border'
        )}
        style={{ backgroundColor: event.color }}
      />

      {/* Tooltip */}
      {isHovered && (
        <div className="absolute bottom-full mb-3 left-1/2 -translate-x-1/2 z-20 animate-in fade-in duration-200">
          <div className="glass-panel px-3 py-2 rounded-lg whitespace-nowrap">
            <p className="text-xs font-bold text-foreground">Chapter {event.chapter}: {event.title}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{event.description}</p>
          </div>

          {/* Arrow pointing down */}
          <div
            className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent"
            style={{
              borderTopColor: 'rgba(26, 31, 41, 0.95)',
            }}
          />
        </div>
      )}
    </div>
  );
}

export function CharacterTimelineView() {
  const [hoveredChapter, setHoveredChapter] = useState<number | null>(null);

  return (
    <div className="glass-panel rounded-xl p-6">
      <h3 className="text-lg font-serif font-bold text-foreground mb-6">Timeline</h3>

      {/* Timeline visualization */}
      <div className="relative mb-8">
        {/* Horizontal line */}
        <div className="absolute top-4 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-border to-transparent" />

        {/* Markers */}
        <div className="flex justify-between px-2 py-0 gap-2">
          {events.map((event) => (
            <TimelineMarker
              key={event.chapter}
              event={event}
              isHovered={hoveredChapter === event.chapter}
              onHover={setHoveredChapter}
            />
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="space-y-2 text-xs">
        <p className="text-muted-foreground font-medium uppercase tracking-wider mb-2">Key Events</p>
        <div className="grid grid-cols-2 gap-2">
          {events.map((event) => (
            <div key={event.chapter} className="flex items-start gap-2">
              <div
                className="w-2 h-2 rounded-full flex-shrink-0 mt-1"
                style={{ backgroundColor: event.color }}
              />
              <div>
                <p className="font-medium text-foreground">Ch. {event.chapter}: {event.title}</p>
                <p className="text-muted-foreground text-xs">{event.character}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
