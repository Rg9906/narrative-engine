'use client';

import React from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { cn } from '@/lib/utils';

interface StatCard {
  label: string;
  value: string | number;
  change: number;
  icon: string;
}

const stats: StatCard[] = [
  { label: 'Total Words', value: '47,250', change: 12, icon: '◆' },
  { label: 'Avg. Quality', value: '87.4%', change: 5, icon: '✦' },
  { label: 'Reading Time', value: '4h 45m', change: 8, icon: '◇' },
  { label: 'Editing Sessions', value: '24', change: 3, icon: '⚙' },
];

const qualityData = [
  { week: 'Week 1', score: 72 },
  { week: 'Week 2', score: 75 },
  { week: 'Week 3', score: 81 },
  { week: 'Week 4', score: 85 },
  { week: 'Week 5', score: 87 },
  { week: 'Week 6', score: 89 },
];

export default function AnalyticsPage() {
  const maxScore = Math.max(...qualityData.map((d) => d.score));

  return (
    <WorkspaceLayout>
      <div className="space-y-12 max-w-6xl mx-auto">
        {/* Header */}
        <PageHeader 
          title="Analytics" 
          subtitle="Project metrics and progress tracking"
          icon="⊡"
        />

        {/* Stats grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <div key={stat.label} className="glass-panel p-6 rounded-xl group hover:scale-105 transition-all duration-300 glow-primary border border-border/30">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">{stat.label}</p>
                  <div className="text-2xl font-bold text-foreground mt-2">{stat.value}</div>
                </div>
                <div className="w-10 h-10 rounded-lg glass-panel flex items-center justify-center text-lg text-primary">
                  {stat.icon}
                </div>
              </div>
              <div className={cn('text-xs font-medium', stat.change > 0 ? 'text-emerald-500' : 'text-red-500')}>
                {stat.change > 0 ? '+' : ''}{stat.change}% from last week
              </div>
            </div>
          ))}
        </div>

        {/* Quality over time chart */}
        <div className="glass-panel p-6 rounded-xl">
          <h2 className="text-lg font-serif font-bold text-foreground mb-6">Quality Score Over Time</h2>

          {/* Simple bar chart */}
          <div className="space-y-4">
            {qualityData.map((data) => (
              <div key={data.week} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-muted-foreground">{data.week}</span>
                  <span className="text-sm font-bold text-foreground">{data.score}%</span>
                </div>
                <div className="w-full h-3 bg-border rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-1000"
                    style={{ width: `${(data.score / maxScore) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Writing insights */}
        <div className="glass-panel p-6 rounded-xl">
          <h2 className="text-lg font-serif font-bold text-foreground mb-6">Writing Insights</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Top strengths */}
            <div className="space-y-4">
              <h3 className="font-serif font-bold text-foreground flex items-center gap-2">
                <span className="text-emerald-500">✓</span> Top Strengths
              </h3>
              <div className="space-y-3">
                {[
                  { label: 'Character Development', score: 92 },
                  { label: 'World Building', score: 88 },
                  { label: 'Dialogue', score: 85 },
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between p-3 bg-emerald-500/5 rounded-lg border border-emerald-500/20">
                    <span className="text-sm text-foreground">{item.label}</span>
                    <span className="text-sm font-bold text-emerald-500">{item.score}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Areas to improve */}
            <div className="space-y-4">
              <h3 className="font-serif font-bold text-foreground flex items-center gap-2">
                <span className="text-yellow-500">⚠</span> Areas to Improve
              </h3>
              <div className="space-y-3">
                {[
                  { label: 'Pacing Control', score: 72 },
                  { label: 'Show vs Tell', score: 68 },
                  { label: 'Formatting', score: 78 },
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between p-3 bg-yellow-500/5 rounded-lg border border-yellow-500/20">
                    <span className="text-sm text-foreground">{item.label}</span>
                    <span className="text-sm font-bold text-yellow-500">{item.score}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Export options */}
        <div className="glass-panel p-6 rounded-xl">
          <h2 className="text-lg font-serif font-bold text-foreground mb-4">Export Report</h2>
          <p className="text-muted-foreground text-sm mb-6">Generate and download a detailed analysis report</p>

          <div className="flex flex-wrap gap-3">
            <button className="px-6 py-3 rounded-lg border border-primary text-primary hover:bg-primary/10 transition-all duration-300 font-medium">
              PDF Report
            </button>
            <button className="px-6 py-3 rounded-lg border border-accent text-accent hover:bg-accent/10 transition-all duration-300 font-medium">
              CSV Data
            </button>
            <button className="px-6 py-3 rounded-lg border border-border text-muted-foreground hover:text-foreground transition-all duration-300 font-medium">
              JSON Export
            </button>
          </div>
        </div>
      </div>
    </WorkspaceLayout>
  );
}
