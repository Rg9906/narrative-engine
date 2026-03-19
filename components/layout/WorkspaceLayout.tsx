'use client';

import React, { ReactNode } from 'react';
import { ParallaxBackground } from './ParallaxBackground';
import { LeftNavRail } from './LeftNavRail';
import { RightIntelligencePanel } from './RightIntelligencePanel';

interface WorkspaceLayoutProps {
  children: ReactNode;
}

export function WorkspaceLayout({ children }: WorkspaceLayoutProps) {
  return (
    <div className="relative w-full h-screen bg-background overflow-hidden">
      {/* Animated background */}
      <ParallaxBackground />

      {/* Left navigation rail */}
      <LeftNavRail />

      {/* Main content area */}
      <main className="ml-20 mr-80 h-screen overflow-auto relative z-10">
        <div className="p-8 min-h-full">
          {children}
        </div>
      </main>

      {/* Right intelligence panel */}
      <RightIntelligencePanel />
    </div>
  );
}
