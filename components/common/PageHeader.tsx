'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  icon?: string;
  action?: React.ReactNode;
}

export function PageHeader({ title, subtitle, icon, action }: PageHeaderProps) {
  return (
    <div className="flex items-start justify-between mb-8 pb-6 border-b border-border/50">
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          {icon && (
            <div className="w-10 h-10 rounded-lg glass-panel flex items-center justify-center glow-primary">
              <span className="text-lg">{icon}</span>
            </div>
          )}
          <h1 className="text-3xl font-serif font-bold text-foreground">{title}</h1>
        </div>
        {subtitle && (
          <p className="text-muted-foreground text-sm">{subtitle}</p>
        )}
      </div>
      {action && (
        <div className="flex items-center gap-2">
          {action}
        </div>
      )}
    </div>
  );
}
