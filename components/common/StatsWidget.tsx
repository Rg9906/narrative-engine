'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface StatItem {
  label: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
}

interface StatsWidgetProps {
  title: string;
  stats: StatItem[];
  className?: string;
}

export function StatsWidget({ title, stats, className }: StatsWidgetProps) {
  return (
    <div className={cn('glass-panel p-6 rounded-lg space-y-6', className)}>
      <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">{title}</h3>
      
      <div className="grid grid-cols-2 gap-4">
        {stats.map((stat, idx) => (
          <div key={idx} className="space-y-2">
            <p className="text-xs text-muted-foreground font-medium">{stat.label}</p>
            <div className="flex items-baseline gap-2">
              <p className="text-xl font-serif font-bold text-foreground">{stat.value}</p>
              {stat.change !== undefined && (
                <span className={cn(
                  'text-xs font-semibold',
                  stat.trend === 'up' ? 'text-emerald-500' : stat.trend === 'down' ? 'text-destructive' : 'text-muted-foreground'
                )}>
                  {stat.trend === 'up' ? '↑' : stat.trend === 'down' ? '↓' : '−'} {Math.abs(stat.change)}%
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
