'use client';

import React from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { SplitViewEditor } from '@/components/editor/SplitViewEditor';

export default function EditorPage() {
  return (
    <WorkspaceLayout>
      <div className="space-y-6 max-w-7xl mx-auto h-full">
        {/* Header */}
        <PageHeader 
          title="Line Editor" 
          subtitle="Manuscript-level editing with AI suggestions"
          icon="✎"
        />

        {/* Editor */}
        <div className="flex-1" style={{ height: 'calc(100vh - 300px)' }}>
          <SplitViewEditor />
        </div>

        {/* Actions */}
        <div className="flex gap-3 justify-end">
          <button className="px-6 py-2 rounded-lg border border-border text-muted-foreground hover:text-foreground transition-colors duration-300">
            Reject All
          </button>
          <button className="px-6 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors duration-300 font-medium">
            Apply Selected
          </button>
          <button className="px-6 py-2 rounded-lg bg-gradient-to-r from-primary to-accent text-white font-medium hover:scale-105 transition-all duration-300">
            Accept All
          </button>
        </div>
      </div>
    </WorkspaceLayout>
  );
}
