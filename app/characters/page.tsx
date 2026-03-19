'use client';

import React from 'react';
import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { CharacterCards } from '@/components/character-system/CharacterCards';
import { CharacterRelationshipGraph } from '@/components/character-system/CharacterRelationshipGraph';
import { CharacterTimelineView } from '@/components/character-system/CharacterTimelineView';

export default function CharactersPage() {
  return (
    <WorkspaceLayout>
      <div className="space-y-12 max-w-6xl mx-auto">
        {/* Header */}
        <PageHeader 
          title="Characters" 
          subtitle="Manage cast and track relationships"
          icon="⚙"
        />

        {/* Character cards */}
        <div className="space-y-4">
          <div>
            <h2 className="text-2xl font-serif font-bold text-foreground">Cast</h2>
          </div>
          <CharacterCards />
        </div>

        {/* Relationship graph and timeline */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <CharacterRelationshipGraph />
          <CharacterTimelineView />
        </div>
      </div>
    </WorkspaceLayout>
  );
}
