'use client';

import React from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { ChapterGrid } from '@/components/dashboard/ChapterGrid';
import { MetricsCards } from '@/components/dashboard/MetricsCards';

export default function DashboardPage() {
  return (
    <WorkspaceLayout>
      <div className="space-y-12 max-w-6xl mx-auto">
        {/* Header */}
        <PageHeader 
          title="Your Story" 
          subtitle="Continue editing and refining your narrative masterpiece"
          icon="◆"
        />

        {/* Metrics */}
        <MetricsCards />

        {/* Chapters */}
        <div className="space-y-4">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Chapters</h2>
            <p className="text-muted-foreground text-sm mt-1">Drag to reorder, click to edit</p>
          </div>
          <ChapterGrid />
        </div>
      </div>
    </WorkspaceLayout>
  );
}
